from flask import request
import logging
from flask_restx import Resource, fields, Namespace
from app.api.services.tokens import check_token
from app.api.services.roles import user_has_rol
from app.api.services.users import (
    get_all_users,
    get_user_by_email,
    add_user,
    get_user_by_id,
    update_user,
    delete_user,
)

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])

users_namespace = Namespace("users")

user = users_namespace.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "name": fields.String(required=True),
        "email": fields.String(required=True),
        "rol": fields.String,
    },
)

user_post = users_namespace.inherit(
    "User post", user, {"password": fields.String(required=True)}
)

parser = users_namespace.parser()
parser.add_argument("Authorization", location="headers")

class UsersList(Resource):
    @users_namespace.marshal_with(user, as_list=True)
    @users_namespace.expect(parser)
    def get(self):
        """Devuelve todos los usuarios."""
        if not user_has_rol(request, "Admin", users_namespace):
            users_namespace.abort(403, "El usuario no es administrador.")
        return get_all_users(), 200

    @users_namespace.expect(user_post, validate=True)
    @users_namespace.response(201, "Se ha creado el usuario <user_email>.")
    @users_namespace.response(400, "El correo ya existe.")
    def post(self):
        """Crea un usuario nuevo."""
        post_data = request.get_json()
        username = post_data.get("name")
        email = post_data.get("email")
        password = post_data.get("password")
        rol = post_data.get("rol")
        response_object = {}

        user = get_user_by_email(email)
        if user:
            response_object["message"] = "El correo ya existe."
            return response_object, 400
        add_user(username, email, password, rol)
        response_object["message"] = f"El usuario {email} se ha creado."
        return response_object, 201

class Users(Resource):
    @users_namespace.marshal_with(user)
    @users_namespace.response(200, "OK")
    @users_namespace.response(404, "El usuario <user_id> no existe.")
    @users_namespace.expect(parser)
    def get(self, user_id):
        """Devuelve un usuario."""
        check_token(request, users_namespace)
        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"El usuario {user_id} no existe.")
        return user, 200

    @users_namespace.expect(user, validate=True)
    @users_namespace.response(200, "El usuario <user_id> se ha actualizado.")
    @users_namespace.response(404, "El usuario <user_id> no existe.")
    def put(self, user_id):
        """Actualiza un usuario."""
        if not user_has_rol(request, "Admin", users_namespace):
            users_namespace.abort(403, "El usuario no es administrador.")
        post_data = request.get_json()
        username = post_data.get("name")
        email = post_data.get("email")
        rol = post_data.get("rol")
        response_object = {}

        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"El usuario {user_id} no existe.")
        update_user(user, username, email, rol)
        response_object["message"] = f"{user.id} actualizado."
        return response_object, 200

    @users_namespace.response(200, "<user_id> eliminado")
    @users_namespace.response(404, "El usuario <user_id> no existe.")
    @users_namespace.expect(parser)
    def delete(self, user_id):
        """Borra un usuario."""
        if not user_has_rol(request, "Admin", users_namespace):
            users_namespace.abort(403, "El usuario no es administrador.")
        response_object = {}
        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"El usuario {user_id} no existe.")
        delete_user(user)
        response_object["message"] = f"{user.email} eliminado."
        return response_object, 200


users_namespace.add_resource(UsersList, "")
users_namespace.add_resource(Users, "/<int:user_id>")
