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
    get_reviews_by_dataset_id_for_process,
    get_review_by_reviewer_and_product
)

reviews_namespace = Namespace("reviews")

reviews = reviews_namespace.model(
    "Review",
    {
        "id": fields.Integer(readOnly=True),
        "datasetId": fields.Integer,
        "productId": fields.String,
        "reviewText": fields.String,
        "reviewTime": fields.DateTime,
        "reviewerId": fields.String,
    },
)
put_parser = reviews_namespace.parser()
put_parser.add_argument("Authorization", location="headers")
put_parser.add_argument("datasetId", location="json")
put_parser.add_argument("productId", location="json")
put_parser.add_argument("reviewText", location="json")
put_parser.add_argument("reviewerId", location="json")

parser = reviews_namespace.parser()
parser.add_argument("Authorization", location="headers")

class ReviewsList(Resource):
    @reviews_namespace.marshal_with(reviews, as_list=True)
    @reviews_namespace.expect(parser)
    def get(self):
        """Devuelve todas las reseñas."""
        check_token(request=request, namespace=reviews_namespace)
        return get_all_reviews(), 200

    @reviews_namespace.marshal_with(reviews)
    @reviews_namespace.response(201, "<review_asin> was added!")
    @reviews_namespace.response(400, "La reseña está duplicada.")
    @reviews_namespace.expect(parser)
    def post(self):
        """Crea una reseña."""
        if not user_has_rol(request, "Admin", reviews_namespace):
            reviews_namespace.abort(403, "El usuario no es administrador.")
        post_data = request.get_json()
        originalId = post_data.get("originalId")
        datasetId = post_data.get("datasetId")
        productId = post_data.get("productId")
        reviewtext = post_data.get("reviewText")
        #TODO: formato de fecha
        reviewtime = post_data.get("reviewTime")
        reviewerid = post_data.get("reviewerId")
        stars = post_data.get("stars")
        response_object = {}
        #TODO: comprobar si ya existe
        review = get_review_by_reviewer_and_product(datasetId=datasetId, reviewer_id=reviewerid, productId=productId)
        if review:
            response_object["message"] = "La reseña está duplicada."
            return response_object, 400
        add_review(datasetId, originalId, productId, reviewtext, reviewtime, reviewerid, stars=stars)
        response_object["message"] = f"La reseña del producto {productId} se ha añadido."
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
        if not user_has_rol(request, "Admin", reviews_namespace):
            reviews_namespace.abort(403, "El usuario no es administrador.")
        post_data = request.get_json()
        reviewText = post_data.get("reviewText")
        response_object = {}

        review = get_review_by_id(review_id)
        if not review:
            reviews_namespace.abort(404, f"La reseña {review_id} no existe.")
        update_review(review, reviewText)
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
        return get_reviews_by_dataset_id_for_process(datasetId=dataset_id), 200

   
    
reviews_namespace.add_resource(ReviewsList, "")
reviews_namespace.add_resource(Reviews, "/<int:review_id>")
reviews_namespace.add_resource(ReviewsListForProcess, "/process/<int:dataset_id>")
