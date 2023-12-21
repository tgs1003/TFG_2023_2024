import json
import pytest
from datetime import datetime
import app.api.views.sentiments

def test_add_sentiment(test_app, monkeypatch):
    def mock_get_old_sentiment(reviewId, model):
        return None
    def mock_add_sentiment(reviewId, stars, sentiment, anger, item, brand, language, source, model, correct, processTime, tokens):
        return True
    
    monkeypatch.setattr(app.api.views.sentiments, "get_get_old_sentiment", mock_get_old_sentiment)
    monkeypatch.setattr(app.api.views.sentiments, "add_sentiment", mock_add_sentiment)
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

def test_add_sentiment_duplicado(test_app, monkeypatch):

    def mock_get_old_sentiment(reviewId, model):
        return True
    def mock_add_sentiment(reviewId, stars, sentiment, anger, item, brand, language, source, model, correct, processTime, tokens):
        return True
    
    monkeypatch.setattr(app.api.views.sentiments, "get_get_old_sentiment", mock_get_old_sentiment)
    monkeypatch.setattr(app.api.views.sentiments, "add_sentiment", mock_add_sentiment)
    

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

def test_add_sentiment_faltan_datos(test_app, monkeypatch):
    def mock_get_old_sentiment(reviewId, model):
        return None
    def mock_add_sentiment(reviewId, stars, sentiment, anger, item, brand, language, source, model, correct, processTime, tokens):
        return True
    
    monkeypatch.setattr(app.api.views.sentiments, "get_old_sentiment", mock_get_old_sentiment)
    monkeypatch.setattr(app.api.views.sentiments, "add_sentiment", mock_add_sentiment)
    
    client = test_app.test_client()
    resp = client.post(
        "/sentiments",
        data=json.dumps(
            {
                "review_id": "review1",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]

def test_get_sentiment_no_existe(test_app, monkeypatch):
    def mock_get_sentiment_by_id(sentiment_id):
        return None
    
    monkeypatch.setattr(app.api.views.sentiments, "get_sentiment_by_id", mock_get_sentiment_by_id)
    
    client = test_app.test_client()
    resp = client.get("/sentiments/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El sentimiento 9990000 no existe" in data["message"]


def test_delete_sentiment_incorrect_id(test_app, monkeypatch):
    def mock_get_sentiment_by_id(sentiment_id):
        return None
    
    monkeypatch.setattr(app.api.views.sentiments, "get_sentiment_by_id", mock_get_sentiment_by_id)
    client = test_app.test_client()
    resp = client.delete("/sentiments/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El sentimiento 9990000 no existe" in data["message"]

def test_update_sentiment_correct(test_app, monkeypatch):
    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self

    def mock_get_sentiment_by_id(sentiment_id):
        d = AttrDict()
        d.update({"id": 1, "review_id": 1,
                  "stars": 5,
                  "sentiment": "positivo",
                  "anger": True,
                  "source": "",
                  "model": "",
                  "creation_date": datetime.now(),
                  "correct": True,
                  "process_time": 2,
                  "tokens": 0
                  })
        return d
    
    def mock_update_sentiment(sentiment, correct):
        return True
    
    monkeypatch.setattr(app.api.views.sentiments, "get_sentiment_by_id", mock_get_sentiment_by_id)
    monkeypatch.setattr(app.api.views.sentiments, "add_sentiment", mock_update_sentiment)

    client = test_app.test_client()
    resp = client.put(f"/sentiments/1", data=json.dumps({
                "correct": False,
            }),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'Sentimiento 1 actualizado.' in data["message"]

