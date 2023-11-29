import datetime
import jwt
import os
from flask import current_app
from app.api.services.users import get_user_by_id
from app.api.models.users import User
import logging

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])

class TokenManager:
    def __init__(self):
        self.access_token_exp = current_app.config.get("ACCESS_TOKEN_EXPIRATION")
        self.refresh_token_exp = current_app.config.get("REFRESH_TOKEN_EXPIRATION")
        self.secret = current_app.config.get("SECRET_KEY")
        self.algorithm = "HS256"

    def encode_token(self, user_id, token_type):
            if token_type == "access":
                seconds = self.access_token_exp
            else:
                seconds = self.refresh_token_exp

            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(
                payload, self.secret, algorithm=self.algorithm
            )

    def decode_token(self, token):
            payload = jwt.decode(token, self.secret, algorithms={self.algorithm})
            return payload["sub"]

class RolManager:
    def check_token(self, request, namespace):
        access_token = request.headers.get("Authorization")
        if access_token:
            try:
                resp = User.decode_token(access_token)
                user = get_user_by_id(resp)
                if not user:
                    namespace.abort(401, "El usuario no existe.")
            except jwt.ExpiredSignatureError:
                    namespace.abort(401,"Token caducado. Vuelva a identificarse.")
            except jwt.InvalidTokenError:
                    namespace.abort(401,"Token no válido")
        else:
            namespace.abort(403,"Hace falta un token.") 
            
    def get_token_user(self, request, namespace):
        access_token = request.headers.get("Authorization")
        if access_token:
            try:
                resp = User.decode_token(access_token)
                user = get_user_by_id(resp)
                if not user:
                    namespace.abort(401, "El usuario no existe.")
                return user
            except jwt.ExpiredSignatureError:
                    namespace.abort(401,"Token caducado. Vuelva a identificarse.")
            except jwt.InvalidTokenError:
                    namespace.abort(401,"Token no válido")
        else:
            namespace.abort(403,"Hace falta un token.") 

    def user_has_rol(self, request, rol, namespace):
        user = self.get_token_user(request=request,namespace=namespace)
        return user.rol == rol

rol_manager = RolManager()
token_manager = TokenManager()
        