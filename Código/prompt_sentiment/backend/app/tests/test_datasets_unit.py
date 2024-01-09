import json
import pytest
import app.api.views.datasets

def test_add_dataset(test_app, monkeypatch):
    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self
    def mock_add_dataset(name, type, config, owner):
        d = AttrDict()
        d.update({"id": 1})
        return d
    
    monkeypatch.setattr(app.api.views.datasets, "add_dataset", mock_add_dataset)
    
    client = test_app.test_client()
    resp = client.post(
        "/datasets",
        data=json.dumps(
            {
                "name": "dataset_prueba1",
                "type": "Huggingface",
                "config": "Prueba/fichero_prueba",
                "owner" : 1
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "Se ha añadido el dataset dataset_prueba1" in data["message"]

def test_get_dataset_no_existe(test_app, monkeypatch):
    def mock_get_dataset_by_id(dataset_id):
        return None
    monkeypatch.setattr(app.api.views.datasets, "get_dataset_by_id", mock_get_dataset_by_id)
    client = test_app.test_client()
    resp = client.get("/datasets/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El dataset 999 no existe" in data["message"]

def test_delete_dataset_incorrect_id(test_app, monkeypatch):
    def mock_get_dataset_by_id(dataset_id):
        return None
    
    monkeypatch.setattr(app.api.views.datasets, "get_dataset_by_id", mock_get_dataset_by_id)
    client = test_app.test_client()
    resp = client.delete("/datasets/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El dataset 999 no existe" in data["message"]

@pytest.mark.parametrize(
    "dataset_id, payload, status_code, message",
    [
        [1, {}, 400, "Input payload validation failed"],
        [1, {"config": "dataset3"}, 400, "Input payload validation failed"],
        [
            999,
            {"status": "Cargado"},
            404,
            "El dataset 999 no existe",
        ],
    ],
)

def test_update_dataset_incorrect_request(test_app, dataset_id, payload, status_code, message, monkeypatch):
    
    def mock_get_dataset_by_id(dataset_id):
        return None
    
    monkeypatch.setattr(app.api.views.datasets, "get_dataset_by_id", mock_get_dataset_by_id)
    client = test_app.test_client()
    resp = client.put(f"/datasets/{dataset_id}", data=json.dumps(payload), content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
