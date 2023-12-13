from flask import request
from flask_restx import Resource, fields, Namespace
from app.api.services.tokens import check_token
from app.api.services.roles import user_has_rol

from app.api.services.review_users import (
get_all_reviewusers,
get_reviewuser_by_id,
add_reviewuser,
update_reviewuser,
delete_reviewuser,
get_reviewusers_with_sentiments)

reviewusers_namespace = Namespace("reviewusers")

reviewusers = reviewusers_namespace.model(
    "ReviewUser",
    {
        "id": fields.String(readOnly=True),
        "name": fields.String,
    },
)

parser = reviewusers_namespace.parser()
parser.add_argument("Authorization", location="headers")

put_parser = reviewusers_namespace.parser()
put_parser.add_argument("Authorization", location="headers")
put_parser.add_argument("id", location="json")
put_parser.add_argument("name", location="json")

class ReviewUserList(Resource):
    @reviewusers_namespace.marshal_with(reviewusers, as_list=True)
    @reviewusers_namespace.expect(parser)
    def get(self):
        """Devuelve todos los usuarios de las reseñas."""
        check_token(request, reviewusers_namespace)
        return get_all_reviewusers(), 200
    
    @reviewusers_namespace.response(201, "El usuario <reviewuser_id> se ha agregado.")
    @reviewusers_namespace.response(400, "El usuario ya existe.")
    @reviewusers_namespace.expect(put_parser)
    @reviewusers_namespace.marshal_with(reviewusers)
    def post(self):
        """Crea un usuario."""
        if not user_has_rol(request, "Admin", reviewusers_namespace):
            reviewusers_namespace.abort(403, "El usuario no es administrador.")
        post_data = request.get_json()
        id = post_data.get("id")
        name = post_data.get("name")
        response_object = {}
        reviewuser = get_reviewuser_by_id(id)
        if reviewuser:
            response_object["message"] = "El usuario ya existe."
            return response_object, 400
        add_reviewuser(reviewuser_id=id, name = name)
        response_object["message"] = f"Se ha añadido el usuario {name}."
        return response_object, 201
    
class ReviewUsersSentiment(Resource):
    @reviewusers_namespace.marshal_with(reviewusers, as_list=True)
    @reviewusers_namespace.expect(parser)
    def get(self):
        """Devuelve todos los usuarios de las reseñas."""
        check_token(request, reviewusers_namespace)
        return get_reviewusers_with_sentiments(), 200

class ReviewUsers(Resource):
    @reviewusers_namespace.marshal_with(reviewusers)
    @reviewusers_namespace.response(200, "Correcto")
    @reviewusers_namespace.response(404, "El usuario <reviewuser_id> no existe.")
    @reviewusers_namespace.expect(parser)
    def get(self, reviewuser_id):
        """Devuelve un usuario."""
        check_token(request, reviewusers_namespace)
        reviewuser = get_reviewuser_by_id(reviewuser_id)
        if not reviewuser:
            reviewusers_namespace.abort(404, f"El usuario {reviewuser_id} no existe.")
        return reviewuser, 200

    @reviewusers_namespace.expect(put_parser, validate=True)
    @reviewusers_namespace.response(200, "Usuario <reviewuser_id> actualizado.")
    @reviewusers_namespace.response(404, "El usuario <reviewuser_id> no existe.")
    def put(self, reviewuser_id):
        """Actualiza un usuario."""
        if not user_has_rol(request, "Admin", reviewusers_namespace):
            reviewusers_namespace.abort(403, "El usuario no es administrador.")
        post_data = request.get_json()
        name = post_data.get("name")
        response_object = {}
        reviewuser = get_reviewuser_by_id(reviewuser_id)
        if not reviewuser:
            reviewusers_namespace.abort(404, f"El usuario {reviewuser_id} no existe.")
        update_reviewuser(reviewuser, name)
        response_object["message"] = f"Usuario {reviewuser.id} actualizado."
        return response_object, 200

    @reviewusers_namespace.response(200, "Usuario <reviewuser_id> eliminado.")
    @reviewusers_namespace.response(404, "El usuario <reviewuser_id> no existe.")
    @reviewusers_namespace.expect(parser)
    def delete(self, reviewuser_id):
        """Borra un usuario."""
        if not user_has_rol(request, "Admin", reviewusers_namespace):
            reviewusers_namespace.abort(403, "El usuario no es administrador.")
        response_object = {}
        reviewuser = get_reviewuser_by_id(reviewuser_id)
        if not reviewuser:
            reviewusers_namespace.abort(404, f"El usuario {reviewuser_id} no existe.")
        delete_reviewuser(reviewuser)
        response_object["message"] = f"El usuario {reviewuser.id} se ha borrado."
        return response_object, 200

reviewusers_namespace.add_resource(ReviewUserList, "")
reviewusers_namespace.add_resource(ReviewUsersSentiment,"/sentiment")
reviewusers_namespace.add_resource(ReviewUsers, "/<string:reviewuser_id>")
