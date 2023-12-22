import json
import pytest
from datetime import datetime

def test_add_review(test_app, test_database, add_user, add_dataset):
    user1 = add_user("justatest1234", "test_review1@test123.com", "greaterthaneight", "Gestor")
    dataset1 = add_dataset(name = "dataset_name", type = "dataset_type", 
                          config = "dataset_config", owner = user1.id)
    client = test_app.test_client()
    resp = client.post(
        "/reviews",
        
        data=json.dumps(
            {
                "dataset_id": dataset1.id,                
                "review_text": "Review Text",
                "review_time": datetime.now().isoformat(),
                "stars": 0
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "La reseña 1 se ha añadido." in data["message"]

def test_add_review_duplicada(test_app, test_database, add_user, add_dataset):
    user1 = add_user("justatest2", "test_review2@test123.com", "greaterthaneight", "Gestor")
    dataset1 = add_dataset(name = "dataset_name", type = "dataset_type", 
                          config = "dataset_config", owner = user1.id)
    client = test_app.test_client()
    resp = client.post(
        "/reviews",
        data=json.dumps(
            {
                "dataset_id": dataset1.id,                
                "review_text": "Review Text",
                "review_time": datetime.now().isoformat(),
                "stars": 0
            }
            
        ),
        content_type="application/json",
    )
    resp = client.post(
        "/reviews",
        data=json.dumps(
            {
                "dataset_id": dataset1.id,                
                "review_text": "Review Text",
                "review_time": datetime.now().isoformat(),
                "stars": 0
            }
            
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "La reseña está duplicada." in data["message"]

def test_add_review_faltan_datos(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/reviews",
        data=json.dumps(
            {
                "dataset_id": 1,
                
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]

def test_add_review_correcto(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/reviews",
        data=json.dumps(
            {
                "dataset_id": 1,
                "review_text": "Review Text3",
                "review_time": datetime.now().isoformat(),
                "stars": 0
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "La reseña 3 se ha añadido." in data["message"]
    
def test_get_review_no_existe(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/reviews/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "La reseña 9990000 no existe" in data["message"]


def test_delete_review(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/reviews/3")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "se ha borrado." in data["message"]

def test_delete_review_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/reviews/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "La reseña 9990000 no existe" in data["message"]

def test_update_review_correct(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(f"/reviews/1", data=json.dumps({
                "dataset_id": "4",
                "review_text": " Review text updated"
            }),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'Reseña 1 actualizada' in data["message"]

@pytest.mark.parametrize(
    "id, payload, status_code, message",
    [
        ["1", {}, 400, "Input payload validation failed"],
        [
            "9990000",
            {"dataset_id": "4",
                
                "review_text": " Review text updated",
                },
            404,
            "La reseña 9990000 no existe",
        ],
    ],
)

def test_update_review_incorrect_request(test_app, test_database, id, payload, status_code, message):
    client = test_app.test_client()
    resp = client.put(f"/reviews/{id}", data=json.dumps(payload),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
