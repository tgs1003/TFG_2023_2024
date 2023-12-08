from sqlalchemy.sql import func
from app import db

class Dataset(db.Model):
    '''
    Modelo de base de datos para la entidad Dataset
    @author: Teodoro Ricardo García Sánchez
    '''
    __tablename__ = 'datasets'
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    name = db.Column(db.String)
    type = db.Column(db.String)
    payload = db.Column(db.String)
    status = db.Column(db.String, default='Creado', nullable=False) #Creado, Cargado, Procesado
    date = db.Column(db.DateTime, server_default=func.now())

