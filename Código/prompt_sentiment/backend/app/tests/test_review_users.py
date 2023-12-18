import json
import pytest

def test_add_review_user(test_app):
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

def test_add_review_user_duplicado(test_app):
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

def test_add_review_user_faltan_datos(test_app):
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

def test_add_review_user_correcto(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/review_users",
        data=json.dumps(
            {
                "id": "user3",
                "name": "username3",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "Se ha añadido el usuario username3" in data["message"]
    assert "username3" in data["name"]
    assert "user3" in data["id"]
    
def test_get_review_user_no_existe(test_app):
    client = test_app.test_client()
    resp = client.get("/review_users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El usuario 999 no existe" in data["message"]


def test_delete_review_user(test_app):
    client = test_app.test_client()
    resp = client.delete("/review_users/user1")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "eliminado" in data["message"]

def test_delete_review_user_incorrect_id(test_app):
    client = test_app.test_client()
    resp = client.delete("/review_users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El usuario 999 no existe" in data["message"]

def test_update_review_user_correct(test_app):
    client = test_app.test_client()
    resp = client.put(f"/review_users/user1", data=json.dumps({
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

def test_update_review_user_incorrect_request(test_app, id, payload, status_code, message):
    client = test_app.test_client()
    resp = client.put(f"/review_users/{id}", data=json.dumps(payload),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
