'''
Código para hacer mantenimiento de la base de datos.
Uso:
python manage.py crear # Crea la base de datos con la definición de las entidades del proyecto
python manage.py recrear # Borra todo y vuelve a crear la estructura de la base de datos
python manage.py rellenar # Rellena la base de datos con la información necesaria para usarla
'''
import os
import sys

from flask.cli import FlaskGroup

from app import create_app, db
from app.api.models.users import User

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('crear')
def create_db():
    engine = create_engine(os.environ.get('DATABASE_URL'))
    if not database_exists(engine.url):
        create_database(engine.url)
        db.create_all()
        db.session.commit()

@cli.command('recrear')
def create_db():
    '''Borra la base de datos y vuelve a empezar'''
    engine = create_engine(os.environ.get('DATABASE_URL'))
    if database_exists(engine.url):
        db.drop_all()
    else:
        create_database(engine.url)
    db.create_all()
    db.session.commit()

@cli.command('rellenar')
def seed_db():
    if db.session.query(User.id).count() == 0:
        """Crea al usuario admin inicial"""
        db.session.add(User(
            name='Admin',
            email='admin',
            password='ubu_1234',
            rol='Admin'
        ))
        db.session.commit()


if __name__ == '__main__':
    cli()
