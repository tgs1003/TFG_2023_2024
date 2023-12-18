import json
import pytest
from datetime import datetime

def test_add_review(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/reviews",
        
        data=json.dumps(
            {
                "originalId": "review1",
                "productId": "product1",
                "reviewText": "Review Text",
                "reviewTime": datetime.now(),
                "reviewerId": "Reviewer id",
                "originalStars": 0
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "La reseña del producto product1 se ha añadido." in data["message"]

def test_add_review_duplicada(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/reviews",
        data=json.dumps(
            {
                "originalId": "review1",
                "productId": "product1",
                "reviewText": "Review Text",
                "reviewTime": datetime.now(),
                "reviewerId": "Reviewer id",
                "originalStars": 0
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "La reseña está duplicada." in data["message"]

def test_add_review_faltan_datos(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/reviews",
        data=json.dumps(
            {
                "originalId": "review1",
                
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]

def test_add_review_correcto(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/reviews",
        data=json.dumps(
            {
                "originalId": "review3",
                "productId": "product3",
                "reviewText": "Review Text3",
                "reviewTime": datetime.now(),
                "reviewerId": "Reviewer id",
                "originalStars": 0
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "La reseña del producto product3 se ha añadido." in data["message"]
    assert "review3" in data["originalId"]
    assert "product3" in data["productId"]
    assert "Review Text3" in data["reviewText"]
    assert "Reviewer id" in data["reviewerId"]
    assert "0" in data["originalStars"]
    
def test_get_review_no_existe(test_app):
    client = test_app.test_client()
    resp = client.get("/reviews/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "La reseña 9990000 no existe" in data["message"]


def test_delete_review(test_app):
    client = test_app.test_client()
    resp = client.delete("/reviews/1")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "se ha borrado." in data["message"]

def test_delete_review_incorrect_id(test_app):
    client = test_app.test_client()
    resp = client.delete("/reviews/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "La reseña 9990000 no existe" in data["message"]

def test_update_review_correct(test_app):
    client = test_app.test_client()
    resp = client.put(f"/reviews/1", data=json.dumps({
                "datasetId": "4",
                "productId": "4updated",
                "reviewText": " Review text updated",
                "reviewerId": "4",
                
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
            {"datasetId": "4",
                "productId": "4updated",
                "reviewText": " Review text updated",
                "reviewerId": "4"},
            404,
            "La reseña 9990000 no existe",
        ],
    ],
)

def test_update_review_incorrect_request(test_app, id, payload, status_code, message):
    client = test_app.test_client()
    resp = client.put(f"/reviews/{id}", data=json.dumps(payload),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
