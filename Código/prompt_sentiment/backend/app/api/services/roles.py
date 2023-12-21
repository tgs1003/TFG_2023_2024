import logging
from flask import current_app
from app.api.services.tokens import get_token_user

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])

def user_has_rol(request, rol, namespace):
    '''
    Devuelve si el usuario del token tiene un rol determinado.
    '''
    if not current_app.config.get("USE_AUTHORIZATION"):
         return True
    user = get_token_user(request = request, namespace = namespace)
    logging.debug(f"user_has_rol, request {request}, rol {rol}, namespace {namespace}")
    return user.rol == rol