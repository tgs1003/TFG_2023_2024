import datetime
from app.api.models.datasets import Dataset

def test_create_dataset(test_app, test_database, add_dataset, add_user):
    user1 = add_user("justatest1234", "test123@test123.com", "greaterthaneight", "Gestor")
    dataset_name ='Prueba1'
    dataset_type ='Huggingface'
    dataset_config='test_config'
    dataset_owner = user1.id
    dataset = add_dataset(name = dataset_name, type = dataset_type, 
                          config = dataset_config, owner = dataset_owner)
    assert dataset.name == dataset_name
    assert dataset.type == dataset_type
    assert dataset.config == dataset_config
    assert dataset.status == 'Creado'
    assert dataset.id != 0
    assert dataset.date < datetime.datetime.now()
    assert dataset.owner == user1.id
