from flask_restx import Api
from jwt import PyJWTError
from psycopg2 import IntegrityError, OperationalError
from app.api.views.auth import auth_namespace
from app.api.views.ping import ping_namespace
from app.api.views.users import users_namespace
from app.api.views.datasets import datasets_namespace
from app.api.views.reviews import reviews_namespace
from app.api.views.sentiments import sentiments_namespace

'''
Configuración de OpenAPI
'''
api = Api(version="1.0", title="Prompt Sentiment API", doc="/swagger")

'''
Aqui registramos los grupos de servicios
'''
api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(users_namespace, path="/users")
api.add_namespace(auth_namespace, path="/auth")
api.add_namespace(datasets_namespace, path="/datasets")
api.add_namespace(reviews_namespace, path="/reviews")
api.add_namespace(sentiments_namespace, path="/sentiments")

@api.errorhandler
def default_error_handler(error):
    #Código de error por defecto
    status_code = getattr(error, 'status_code', 500)

    if isinstance(error, PyJWTError):
        return {"message": str(error)}, 401

    elif type(error) in [OperationalError, IntegrityError]:
        return {"message": "Error de base de datos."}, status_code

    else:
        return {"message": str(error)}, status_code