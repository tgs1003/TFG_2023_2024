import logging
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
    user = get_token_user(request = request, namespace = namespace)
    return user.rol == rol