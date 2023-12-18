import json
import pytest
from datetime import datetime
import app.api.views.reviews

def test_add_review(test_app, monkeypatch):

    def mock_get_review_by_reviewer_and_product(datasetId, reviewer_id, productId):
        return None
    def mock_add_review(datasetId, originalId, productId, reviewtext, reviewtime, reviewerid, stars):
        return True
    
    monkeypatch.setattr(app.api.views.reviews, "get_review_by_reviewer_and_product", mock_get_review_by_reviewer_and_product)
    monkeypatch.setattr(app.api.views.reviews, "add_review", mock_add_review)
   
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

def test_add_review_duplicada(test_app, monkeypatch):
    def mock_get_review_by_reviewer_and_product(datasetId, reviewer_id, productId):
        return True
    def mock_add_review(datasetId, originalId, productId, reviewtext, reviewtime, reviewerid, stars):
        return True
    
    monkeypatch.setattr(app.api.views.reviews, "get_review_by_reviewer_and_product", mock_get_review_by_reviewer_and_product)
    monkeypatch.setattr(app.api.views.reviews, "add_review", mock_add_review)

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

def test_add_reviewfaltan_datos(test_app, monkeypatch):

    def mock_get_review_by_reviewer_and_product(datasetId, reviewer_id, productId):
        return True
    def mock_add_review(datasetId, originalId, productId, reviewtext, reviewtime, reviewerid, stars):
        return True
    
    monkeypatch.setattr(app.api.views.reviews, "get_review_by_reviewer_and_product", mock_get_review_by_reviewer_and_product)
    monkeypatch.setattr(app.api.views.reviews, "add_review", mock_add_review)
  
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
    def mock_delete_review(reviewId):
        return None

    monkeypatch.setattr(app.api.views.reviews, "delete_review", mock_delete_review)
  
    client = test_app.test_client()
    resp = client.delete("/reviews/9990000")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "La reseña 9990000 no existe" in data["message"]

def test_update_review_correct(test_app, monkeypatch):
    def mock_get_review_by_id(review_id):
        return True
    def mock_update_review(review, reviewText):
        return True
    
    monkeypatch.setattr(app.api.views.reviews, "get_review_by_id", mock_get_review_by_id)
    monkeypatch.setattr(app.api.views.reviews, "update_review", mock_update_review)
    
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
