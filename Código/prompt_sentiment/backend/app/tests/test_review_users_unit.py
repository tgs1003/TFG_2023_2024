import json
import pytest
import app.api.views.review_users

import json
import pytest

def test_add_review_user(test_app, monkeypatch):
    
    def mock_get_reviewuser_by_id(productId):
        return None
    def mock_add_reviewuser(productId, title):
        return True
    
    monkeypatch.setattr(app.api.views.review_users, "get_reviewuser_by_id", mock_get_reviewuser_by_id)
    monkeypatch.setattr(app.api.views.review_users, "add_reviewuser", mock_add_reviewuser)
    
    client = test_app.test_client()
    resp = client.post(
        "/review_users",
        
        data=json.dumps(
            {
                "id": "user1",
                "name": "username1",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "Se ha añadido el usuario user_name1" in data["message"]

def test_add_review_user_duplicado(test_app, monkeypatch):
    
    def mock_get_reviewuser_by_id(reviewuser_id):
        return None
    def mock_add_reviewuser(reviewuser_id, name):
        return True
    
    monkeypatch.setattr(app.api.views.review_users, "get_reviewuser_by_id", mock_get_reviewuser_by_id)
    monkeypatch.setattr(app.api.views.review_users, "add_reviewuser", mock_add_reviewuser)
    
    client = test_app.test_client()
    resp = client.post(
        "/review_users",
        data=json.dumps(
            {
                "id": "user1",
                "name": "username2",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "El usuario ya existe." in data["message"]

def test_add_review_user_faltan_datos(test_app, monkeypatch):
    
    def mock_get_reviewuser_by_id(reviewuser_id):
        return None
    def mock_add_reviewuser(reviewuser_id, name):
        return True
    
    monkeypatch.setattr(app.api.views.review_users, "get_reviewsuer_by_id", mock_get_reviewuser_by_id)
    monkeypatch.setattr(app.api.views.review_users, "add_reviewuser", mock_add_reviewuser)
    
    client = test_app.test_client()
    resp = client.post(
        "/review_users",
        data=json.dumps(
            {
                "id": "user2",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]
    
def test_get_review_user_no_existe(test_app, monkeypatch):
    
    def mock_get_reviewuser_by_id(reviewuser_id):
        return None
    
    monkeypatch.setattr(app.api.views.review_users, "get_reviewsuer_by_id", mock_get_reviewuser_by_id)
    client = test_app.test_client()
    resp = client.get("/review_user/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El usuario 999 no existe" in data["message"]


def test_delete_review_user_incorrect_id(test_app, monkeypatch):
    def mock_get_reviewuser_by_id(reviewuser_id):
        return None
    
    monkeypatch.setattr(app.api.views.review_users, "get_reviewsuer_by_id", mock_get_reviewuser_by_id)
  
    client = test_app.test_client()
    resp = client.get("/review_user/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El usuario 999 no existe" in data["message"]

def test_update_review_user_correct(test_app, monkeypatch):
    
    def mock_get_reviewuser_by_id(reviewuser_id):
        return True
    
    def mock_update_reviewuser(reviewuser, name):
        return True
    
    monkeypatch.setattr(app.api.views.review_users, "get_reviewsuer_by_id", mock_get_reviewuser_by_id)
    monkeypatch.setattr(app.api.views.review_users, "update_reviewsuer", mock_update_reviewuser)
    
    client = test_app.test_client()
    resp = client.put(f"/review_user/user1", data=json.dumps({
                "name": "review_user_modified",
            }),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'Usuario user1 actualizado' in data["message"]

@pytest.mark.parametrize(
    "id, payload, status_code, message",
    [
        ["user1", {}, 400, "Input payload validation failed"],
        [
            "user999",
            {"name": "username_999"},
            404,
            "El producto 999 no existe",
        ],
    ],
)

def test_update_review_user_incorrect_request(test_app, id, payload, status_code, message, monkeypatch):
    
    def mock_get_reviewuser_by_id(reviewuser_id):
        return None
    
    monkeypatch.setattr(app.api.views.review_users, "get_reviewsuer_by_id", mock_get_reviewuser_by_id)
    
    client = test_app.test_client()
    resp = client.put(f"/review_user/{id}", data=json.dumps(payload),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
