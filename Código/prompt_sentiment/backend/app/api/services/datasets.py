from app import db
from app.api.models.datasets import Dataset

def get_all_datasets():
    '''
    Devuelve todos los datasets
    '''
    return Dataset.query.all()

def get_dataset_by_id(id):
    '''
    Devuelve un dataset
    '''
    return Dataset.query.filter_by(id=id).first()

def get_dataset_by_payload(payload):
    '''
    Busca un dataset con el mismo payload
    '''
    return Dataset.query.filter_by(payload=payload).first()

def add_dataset(name, type, payload):
    '''
    Agrega un dataset
    '''
    dataset = Dataset(name=name, type=type, payload=payload, status="Creado")
    db.session.add(dataset)
    db.session.commit()
    return dataset

def update_dataset(dataset, status):
    '''
    Actualiza un dataset
    '''
    dataset.status = status
    db.session.commit()
    return dataset

def delete_dataset(dataset):
    '''
    Borra un dataset
    '''
    db.session.delete(dataset)
    db.session.commit()
    return dataset