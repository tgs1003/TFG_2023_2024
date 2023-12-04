import jwt
from flask import request
from flask_restx import Namespace, Resource, fields
from app import bcrypt
from app.api.services.tokens import get_token_user, encode_token, decode_token
from app.api.services.users import get_user_by_email, get_user_by_id, add_user

auth_namespace = Namespace("auth")

user = auth_namespace.model(
    "User",
    {"username": fields.String(required=True), "email": fields.String(required=True), "rol": fields.String},
)

full_user = auth_namespace.inherit(
    "Full User", user, {"password": fields.String(required=True)}
)

login = auth_namespace.model(
    "User",
    {"email": fields.String(required=True), "password": fields.String(required=True)},
)

refresh = auth_namespace.model(
    "Refresh", {"refresh_token": fields.String(required=True)}
)

tokens = auth_namespace.inherit(
    "Access and refresh_tokens", refresh, {"access_token": fields.String(required=True)}
)

'''
Cabecera para pedir el token de autorización
'''
parser = auth_namespace.parser()
parser.add_argument("Authorization", location="headers")

class Register(Resource):
    '''
    Clase para el registro de un usuario
    '''
    @auth_namespace.marshal_with(user)
    @auth_namespace.expect(full_user, validate=True)
    @auth_namespace.response(201, "Petición procesada correctamente.")
    @auth_namespace.response(400, "El correo ya existe.")
    def post(self):
        post_data = request.get_json()
        name = post_data.get("name")
        email = post_data.get("email")
        password = post_data.get("password")
        user = get_user_by_email(email)
        if user:
            auth_namespace.abort(400, "El correo ya existe.")
        user = add_user(name, email, password)
        return user, 201

class Login(Resource):
    '''
    Clase para autenticarse en la aplicación
    Devuelve 2 tokens uno de acceso y otro de refresco.
    Cuando caduque el de acceso se puede pedir otro usando el de refresco.
    '''
    @auth_namespace.marshal_with(tokens)
    @auth_namespace.expect(login, validate=True)
    @auth_namespace.response(200, "Petición procesada correctamente.")
    @auth_namespace.response(404, "El usuario no existe.")
    def post(self):
        post_data = request.get_json()
        email = post_data.get("email")
        password = post_data.get("password")
        response_object = {}
        
        user = get_user_by_email(email)
        if not user or not bcrypt.check_password_hash(user.password, password):
            auth_namespace.abort(404, "El usuario no existe.")

        access_token = encode_token(user.id, "access")
        refresh_token = encode_token(user.id, "refresh")

        response_object = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return response_object, 200

class Refresh(Resource):
    '''
    Devuelve otro token usando el token de refresco.
    '''
    @auth_namespace.marshal_with(tokens)
    @auth_namespace.expect(refresh, validate=True)
    @auth_namespace.response(200, "Petición procesada correctamente.")
    @auth_namespace.response(401, "Token no válido.")
    def post(self):
        post_data = request.get_json()
        refresh_token = post_data.get("refresh_token")
        response_object = {}

        try:
            resp = decode_token(refresh_token)
            user = get_user_by_id(resp)
            if not user:
                auth_namespace.abort(401, "Token no válido.")
            access_token = encode_token(user.id, "access")
            refresh_token = encode_token(user.id, "refresh")

            response_object = {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
            return response_object, 200
        except jwt.ExpiredSignatureError:
            auth_namespace.abort(401, "Firma caducada, vuelva a autenticarse.")
            return "Firma caducada, vuelva a autenticarse."
        except jwt.InvalidTokenError:
            auth_namespace.abort(401, "Token no válido, vuelva a autenticarse.")

class Status(Resource):
    '''
    Comprueba que el token es correcto y devuelve el usuario logado
    Se puede usar para comprobar que todo funciona correctamente.
    '''
    @auth_namespace.marshal_with(user)
    @auth_namespace.response(200, "Petición procesada correctamente.")
    @auth_namespace.response(401, "Token no válido.")
    @auth_namespace.expect(parser)
    def get(self):
        return get_token_user(request=request, namespace=auth_namespace)

'''
Aquí se registran las urls del servicio
'''        
auth_namespace.add_resource(Register, "/register")
auth_namespace.add_resource(Login, "/login")
auth_namespace.add_resource(Refresh, "/refresh")
auth_namespace.add_resource(Status, "/status")
