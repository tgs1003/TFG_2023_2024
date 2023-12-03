import datetime
import jwt
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

def encode_token(user_id, token_type):
    '''
    Cifra un token usando una clave secreta (SECRET_KEY)
    '''
    if token_type == "access":
        seconds = current_app.config.get("ACCESS_TOKEN_EXPIRATION")
    else:
        seconds = current_app.config.get("REFRESH_TOKEN_EXPIRATION")

    #En el token se incluye la hora de creación, la de caducidad y el usuario para el que se emitido el token.
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds),
        "iat": datetime.datetime.utcnow(),
        "sub": user_id,
    }
    return jwt.encode(
        payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
    )

def decode_token(token):
    '''
    Descifra un token usando una clave secreta (SECRET_KEY)
    '''
    payload = jwt.decode(token, current_app.config.get("SECRET_KEY"), algorithms={"HS256"})
    return payload["sub"]

def check_token(request, namespace):
    '''
    Comprueba si el token es válido y si el usuario está dado de alta en el sistema.
    '''
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
                namespace.abort(401,"Token no válido.")
    else:
        namespace.abort(403,"Hace falta un token.") 
        
def get_token_user(request, namespace):
    '''
    Devuelve el usuario que está logado en el sistema (según la información del token)
    '''
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