import json
import pytest
from datetime import datetime

def test_add_sentiment(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/sentiments",
        
        data=json.dumps(
            {
                "reviewId": 2,
                "stars": 0,
                "sentiment": "positive",
                "anger": False,
                "item": "unknown",
                "brand": "unknown",
                "language": "en",
                "source":"",
                "model":"OpenAI",
                "correct": True,
                "processTime": 6,
                "tokens": 0
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "Se ha añadido el sentimento para la reseña 2." in data["message"]

def test_add_sentiment_duplicado(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/sentiments",
        data=json.dumps(
            {
                "reviewId": 2,
                "stars": 0,
                "sentiment": "positive",
                "anger": False,
                "item": "unknown",
                "brand": "unknown",
                "language": "en",
                "source":"",
                "model":"OpenAI",
                "correct": True,
                "processTime": 6,
                "tokens": 0
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "El sentimiento ya existe." in data["message"]

def test_add_sentiment_faltan_datos(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/sentiments",
        data=json.dumps(
            {
                "reviewId": "review1",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]

def test_add_sentiment_correcto(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/sentiments",
        data=json.dumps(
            {
                "reviewId": 2,
                "stars": 0,
                "sentiment": "positive",
                "anger": False,
                "item": "unknown",
                "brand": "unknown",
                "language": "en",
                "source":"",
                "model":"OpenAI",
                "correct": True,
                "processTime": 6,
                "tokens": 0
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "Se ha añadido el sentimiento para la reseña 2." in data["message"]
    assert data["stars"] == 0
    assert "positive" in data["sentiment"]
    assert data["anger"] == False
    assert "unknown" in data["item"]
    assert "unknown" in data["brand"]
    assert "en" in data["language"]
    assert "OpenAI" in data["model"]
    assert data["correct"] == True
    assert data["tokens"] == 0
    
def test_get_sentiment_no_existe(test_app):
    client = test_app.test_client()
    resp = client.get("/sentiments/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El sentimiento 9990000 no existe" in data["message"]


def test_delete_sentiment(test_app):
    client = test_app.test_client()
    resp = client.delete("/sentiments/1")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "El sentimento 1 se ha borrado." in data["message"]

def test_delete_sentiment_incorrect_id(test_app):
    client = test_app.test_client()
    resp = client.delete("/sentiments/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El sentimento 9990000 no existe" in data["message"]

def test_update_sentiment_correct(test_app):
    client = test_app.test_client()
    resp = client.put(f"/sentiments/1", data=json.dumps({
                "correct": False,
            }),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'Sentimento 1 actualizado' in data["message"]

@pytest.mark.parametrize(
    "id, payload, status_code, message",
    [
        ["1", {}, 400, "Input payload validation failed"],
        [
            "9990000",
            {
                "correct": False
            },
            404,
            "La reseña 9990000 no existe",
        ],
    ],
)

def test_update_sentiment_incorrect_request(test_app, id, payload, status_code, message):
    client = test_app.test_client()
    resp = client.put(f"/sentiments/{id}", data=json.dumps(payload),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
