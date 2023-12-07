import datetime
from app.api.models.datasets import Dataset

def test_create_dataset(add_dataset):
    dataset_name ='Prueba1'
    dataset_type ='Huggingface'
    dataset_payload='test_payload'
    dataset = add_dataset(dataset_name, dataset_type, dataset_payload)
    assert dataset.name == dataset_name
    assert dataset.type == dataset_type
    assert dataset.payload == dataset_payload
    assert dataset.status == 0
    assert dataset.id != 0
    assert dataset.date > datetime.datetime.now()
