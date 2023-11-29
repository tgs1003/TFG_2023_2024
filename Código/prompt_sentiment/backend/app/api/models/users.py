from flask import current_app
from sqlalchemy.sql import func
from app import db, bcrypt

class User(db.Model):
    """
    Modelo de la entidad "User" para la gestión de usuarios de la aplicación.
    @author: Teodoro Ricardo García Sánchez
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    name = db.Column(db.String(1000))
    rol = db.Column(db.String(100))
    date = db.Column(db.DateTime, server_default=func.now())

    def __init__(self, name="", email="", password="", rol = ""):
        self.name = name
        self.email = email
        self.rol = rol
        #Calculamos el hash de la contraseña para almacenarlo en la base de datos.
        #De esta forma es imposible saber cual es la contraseña pero se puede verificar si es correcta.
        #Lo calculamos con la librería Bcrypt, el parámetro BCRYPT_LOG_ROUNDS se refiere al número de iteraciones
        #que se realizan para calcular el hash. Un número más es más seguro pero tarda más.
        #Ver: https://bcrypt.sourceforge.net/
        self.password = bcrypt.generate_password_hash(password, current_app.config.get("BCRYPT_LOG_ROUNDS")).decode('utf-8')

    