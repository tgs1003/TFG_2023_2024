import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Inicializamos SQLAlchemy
db = SQLAlchemy()
cors = CORS()
bcrypt  = Bcrypt()


def create_app():
    # Creamos una instancia de Flask en el módulo actual
    app = Flask(__name__)
    # Cargamos la configuración
    app_settings = os.getenv("APP_SETTINGS","app.config.DevelopmentConfig")
    app.config.from_object(app_settings)
    # Inicializamos la base de datos
    db.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})
    bcrypt.init_app(app)

    from app.api import api
    api.init_app(app)

    return app

