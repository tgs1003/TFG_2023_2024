'''
Servicios para interactuar con los usuarios de base de datos
'''
from app import db
from app.api.models.users import User

def get_all_users():
    '''
    Devuelve todos los usuarios registrados en la base de datos
    '''
    return User.query.all()

def get_user_by_id(user_id):
    '''
    Devuelve el usuario identificado con user_id
    '''
    return User.query.filter_by(id = user_id).first()

def get_user_by_email(email):
    '''
    Devuelve un usuario que coincida con el correo especificado
    '''
    return User.query.filter_by(email = email).first()

def add_user(name, email, password, rol):
    '''
    Agrega un usuario a la base de datos
    '''
    user = User(name = name, email = email, password = password, rol = rol)
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user, username, email, rol):
    '''
    Actualiza los datos de un usuario
    '''
    user.name = username
    user.email = email
    user.rol = rol
    db.session.commit()
    return user

def delete_user(user):
    '''
    Borra el usuario especificado
    '''
    db.session.delete(user)
    db.session.commit()
    return user
