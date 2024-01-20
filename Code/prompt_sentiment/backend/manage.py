'''
Código para hacer mantenimiento de la base de datos.
Uso:
python manage.py crear # Crea la base de datos con la definición de las entidades del proyecto
python manage.py recrear # Borra todo y vuelve a crear la estructura de la base de datos
python manage.py rellenar # Rellena la base de datos con la información necesaria para usarla
'''
import os
from flask.cli import FlaskGroup
from app import create_app, db
from app.api.models.users import User
from app.api.models.datasets import Dataset

import logging
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(), override=True) # read local .env file

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('crear')
def create_db():
    engine = create_engine(os.environ.get('DATABASE_URL'))
    logging.debug(os.environ.get('DATABASE_URL'))
    if not database_exists(engine.url):
        create_database(engine.url)
        db.create_all()
        db.session.commit()

@cli.command('crear_test')
def create_test_db():
    engine = create_engine(os.environ.get('TEST_DATABASE_URL'))
    logging.debug(os.environ.get('TEST_DATABASE_URL'))
    if not database_exists(engine.url):
        create_database(engine.url)
        db.create_all()
        db.session.commit()

@cli.command('recrear')
def recreate_db():
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
        user = User(
            name='Admin',
            email='admin@promptsentiment.es',
            password='ubu_1234',
            rol='Admin'
        )
        db.session.add(user)
        db.session.commit()
        # Creamos un dataset de prueba
        db.session.add(Dataset(name='Amazon Shoe Reviews (test)', type='Hugging face', config='{ \
        "name": "Amazon Shoe Reviews", \
        "type": "Hugging face", \
        "path":"mesmalif/amazon-shoe-reviews",\
        "subset": "test",\
        "mapping": { \
        "review_text": "text", \
        "review_headline": "review_headline", \
        "stars": "labels", \
        "review_id": "review_id", \
        "review_date": "review_date" \
            }, \
        "correct_stars": 0,\
        "date_format": "%Y-%m-%d"\
        }', status='Creado', owner = user.id))

        db.session.commit()


if __name__ == '__main__':
    cli()
