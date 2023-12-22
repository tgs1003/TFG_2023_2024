from flask import request
from flask_restx import Resource, fields, Namespace
from app.api.services.tokens import check_token
from app.api.services.roles import user_has_rol
from app.api.services.reviews import (
    get_all_reviews, 
    get_review_by_id, 
    add_review,
    update_review,
    delete_review,
    get_reviews_by_dataset_id,
    get_review_by_dataset_id_and_review_text
)

reviews_namespace = Namespace("reviews")

reviews = reviews_namespace.model(
    "Review",
    {
        "id": fields.Integer(readOnly=True),
        "dataset_id": fields.Integer,
        "review_text": fields.String,
        "review_time": fields.DateTime,
    },
)
put_parser = reviews_namespace.parser()
put_parser.add_argument("Authorization", location="headers")
put_parser.add_argument("dataset_id", location="json")
put_parser.add_argument("review_text", location="json", required=True)

post_parser = reviews_namespace.parser()
post_parser.add_argument("Authorization", location="headers")
post_parser.add_argument("dataset_id", location="json", required=True)
post_parser.add_argument("review_text", location="json", required=True)
post_parser.add_argument("review_time", location="json")
post_parser.add_argument("stars", location="json")


parser = reviews_namespace.parser()
parser.add_argument("Authorization", location="headers")

class ReviewsList(Resource):
    @reviews_namespace.marshal_with(reviews, as_list=True)
    @reviews_namespace.expect(parser)
    def get(self):
        """Devuelve todas las reseñas."""
        check_token(request=request, namespace=reviews_namespace)
        return get_all_reviews(), 200

    
    @reviews_namespace.response(201, "<review_id> was added!")
    @reviews_namespace.response(400, "La reseña está duplicada.")
    @reviews_namespace.expect(post_parser)
    def post(self):
        """Crea una reseña."""
        data = post_parser.parse_args(request)
        if not user_has_rol(request, "Admin", reviews_namespace):
            reviews_namespace.abort(403, "El usuario no es administrador.")
        dataset_id = data["dataset_id"]
        review_text = data["review_text"]
        #TODO: formato de fecha
        review_time = data["review_time"]
        stars = data["stars"]
        response_object = {}
        #TODO: comprobar si ya existe
        review = get_review_by_dataset_id_and_review_text(dataset_id = dataset_id, review_text = review_text)
        if review:
            response_object["message"] = "La reseña está duplicada."
            return response_object, 400
        review = add_review(dataset_id, review_text, review_time, original_stars=stars)
        response_object["message"] = f"La reseña {review.id} se ha añadido."
        return response_object, 201

class Reviews(Resource):
    @reviews_namespace.marshal_with(reviews)
    @reviews_namespace.response(200, "Correcto")
    @reviews_namespace.response(404, "La reseña <review.id> no existe.")
    @reviews_namespace.expect(parser)
    def get(self, review_id):
        """Devuelve una reseña."""
        check_token(request=request, namespace=reviews_namespace)
        review = get_review_by_id(review_id)
        if not review:
            reviews_namespace.abort(404, f"La reseña {review_id} no existe.")
        return review, 200

    @reviews_namespace.expect(put_parser, validate=True)
    @reviews_namespace.response(200, "Reseña <review_id> actualizada.")
    @reviews_namespace.response(404, "La reseña <review_id> no existe.")
    def put(self, review_id):
        """Actualiza la reseña."""
        data = put_parser.parse_args(request)
        if not user_has_rol(request, "Admin", reviews_namespace):
            reviews_namespace.abort(403, "El usuario no es administrador.")
        review_text = data["review_text"]
        response_object = {}

        review = get_review_by_id(review_id)
        if not review:
            reviews_namespace.abort(404, f"La reseña {review_id} no existe.")
        update_review(review, review_text)
        response_object["message"] = f"Reseña {review.id} actualizada."
        return response_object, 200

    @reviews_namespace.response(200, "<review_id> eliminada.")
    @reviews_namespace.response(404, "La reseña <review_id> no existe.")
    @reviews_namespace.expect(parser)
    def delete(self, review_id):
        """Borra una reseña."""
        if not user_has_rol(request, "Admin", reviews_namespace):
            reviews_namespace.abort(403, "El usuario no es administrador.")
        response_object = {}
        review = get_review_by_id(review_id)
        if not review:
            reviews_namespace.abort(404, f"La reseña {review_id} no existe.")
        delete_review(review)
        response_object["message"] = f"La reseña {review.id} se ha borrado."
        return response_object, 200
    
class ReviewsListForProcess(Resource):
    @reviews_namespace.marshal_with(reviews, as_list=True)
    @reviews_namespace.expect(parser)
    def get(self, dataset_id):
        """Devuelve todas las reseñas."""
        check_token(request=request, namespace=reviews_namespace)
        return get_reviews_by_dataset_id(datasetId=dataset_id), 200

   
    
reviews_namespace.add_resource(ReviewsList, "")
reviews_namespace.add_resource(Reviews, "/<int:review_id>")
reviews_namespace.add_resource(ReviewsListForProcess, "/process/<int:dataset_id>")
