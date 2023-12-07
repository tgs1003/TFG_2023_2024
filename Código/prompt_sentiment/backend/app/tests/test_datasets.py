import json
import pytest

def test_add_dataset(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/datasets",
        data=json.dumps(
            {
                "name": "dataset_prueba1",
                "type": "Huggingface",
                "payload": "Prueba/fichero_prueba",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "Se ha añadido el dataset dataset_prueba1" in data["message"]

def test_add_dataset_duplicado(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/datasets",
        data=json.dumps(
            {
                "name": "dataset_prueba1",
                "type": "Huggingface",
                "payload": "Prueba/fichero_prueba",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "El dataset ya existe" in data["message"]

def test_add_dataset_faltan_datos(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/datasets",
        data=json.dumps(
            {
                "type": "Huggingface",
                "payload": "Prueba/fichero_prueba",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]

def test_add_dataset_correcto(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/datasets",
        data=json.dumps(
            {
                "name": "dataset_prueba2",
                "type": "Huggingface",
                "payload": "Prueba/fichero_prueba2",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "Se ha añadido el dataset dataset_prueba2" in data["message"]
    assert "dataset_prueba2" in data["name"]
    assert "Huggingface" in data["type"]
    assert "Prueba/fichero_prueba2" in data["payload"]
    assert "0" in data["status"]
    assert "id" in data

def test_add_dataset_no_existe(test_app):
    client = test_app.test_client()
    resp = client.get("/datasets/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El dataset 999 no existe" in data["message"]


def test_delete_dataset(test_app):
    client = test_app.test_client()
    resp = client.get("/datasets/1")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "eliminado" in data["message"]

def test_delete_dataset_incorrect_id(test_app):
    client = test_app.test_client()
    resp = client.get("/datasets/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El dataset 999 no existe" in data["message"]

def test_update_dataset_correct(test_app):
    client = test_app.test_client()
    resp = client.put(f"/datasets/2", data=json.dumps({
                "status": "1",
            }),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'Dataset 2 actualizado' in data["message"]

@pytest.mark.parametrize(
    "datasetid, payload, status_code, message",
    [
        [1, {}, 400, "Input payload validation failed"],
        [1, {"name": "dataset3"}, 400, "Input payload validation failed"],
        [
            999,
            {"status": "1"},
            404,
            "El dataset 999 no existe",
        ],
    ],
)

def test_update_dataset_incorrect_request(test_app, dataset_id, payload, status_code, message):
    client = test_app.test_client()
    resp = client.put(f"/datasets/{dataset_id}", data=json.dumps(payload),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
