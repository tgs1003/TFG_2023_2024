import json
import pytest
from datetime import datetime
import app.api.views.reviews

def test_add_review(test_app, monkeypatch):
    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self

    def mock_get_review_by_dataset_id_and_review_text(dataset_id, review_text):
        return None
    def mock_add_review(dataset_id, review_text, review_time, original_stars):
        d = AttrDict()
        d.update({"id": 1})
        return d
    
    monkeypatch.setattr(app.api.views.reviews, "get_review_by_dataset_id_and_review_text", mock_get_review_by_dataset_id_and_review_text)
    monkeypatch.setattr(app.api.views.reviews, "add_review", mock_add_review)
   
    client = test_app.test_client()
    resp = client.post(
        "/reviews",
        
        data=json.dumps(
            {
                "dataset_id": 1,
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

def test_add_review_duplicada(test_app, monkeypatch):
    def mock_get_review_by_dataset_id_and_review_text(dataset_id, review_text):
        return True
    def mock_add_review(dataset_id, review_text, review_time, original_stars):
        return True
    
    monkeypatch.setattr(app.api.views.reviews, "get_review_by_dataset_id_and_review_text", mock_get_review_by_dataset_id_and_review_text)
    monkeypatch.setattr(app.api.views.reviews, "add_review", mock_add_review)

    client = test_app.test_client()
    resp = client.post(
        "/reviews",
        data=json.dumps(
            {
                "dataset_id": 1,
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

def test_add_reviewfaltan_datos(test_app, monkeypatch):

    def mock_get_review_by_dataset_id_and_review_text(dataset_id, review_text):
        return True
    def mock_add_review(dataset_id, review_text, review_time, original_stars):
        return True
    
    monkeypatch.setattr(app.api.views.reviews, "get_review_by_dataset_id_and_review_text", mock_get_review_by_dataset_id_and_review_text)
    monkeypatch.setattr(app.api.views.reviews, "add_review", mock_add_review)
  
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

    
def test_get_review_no_existe(test_app, monkeypatch):
    def mock_get_review_by_id(reviewId):
        return None

    monkeypatch.setattr(app.api.views.reviews, "get_review_by_id", mock_get_review_by_id)
    
    client = test_app.test_client()
    resp = client.get("/reviews/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "La reseña 9990000 no existe" in data["message"]


def test_delete_review_incorrect_id(test_app, monkeypatch):
    def mock_get_review_by_id(review_id):
        return None
    def mock_delete_review(review_id):
        return None

    monkeypatch.setattr(app.api.views.reviews, "get_review_by_id", mock_get_review_by_id)
    monkeypatch.setattr(app.api.views.reviews, "delete_review", mock_delete_review)
  
    client = test_app.test_client()
    resp = client.delete("/reviews/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "La reseña 9990000 no existe" in data["message"]

def test_update_review_correct(test_app, monkeypatch):
    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self

    def mock_get_review_by_id(review_id):
        d = AttrDict()
        d.update({"id": 1})
        return d
    def mock_update_review(review, review_text):
        return True
    
    monkeypatch.setattr(app.api.views.reviews, "get_review_by_id", mock_get_review_by_id)
    monkeypatch.setattr(app.api.views.reviews, "update_review", mock_update_review)
    
    client = test_app.test_client()
    resp = client.put(f"/reviews/1", data=json.dumps({
                "dataset_id": "4",
                "review_text": " Review text updated",
                
                
            }),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'Reseña 1 actualizada' in data["message"]
