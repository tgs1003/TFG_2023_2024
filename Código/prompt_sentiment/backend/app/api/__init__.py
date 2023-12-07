from flask_restx import Api
from app.api.views.auth import auth_namespace
from app.api.views.ping import ping_namespace
from app.api.views.users import users_namespace
from app.api.views.datasets import datasets_namespace

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
