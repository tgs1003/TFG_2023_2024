import json
import pytest


def test_registro_usuario(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(
            {"username": "prueba1", "email": "prueba@correo.com", "password": "123456"}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert resp.content_type == "application/json"
    assert "prueba1" in data["username"]
    assert "prueba@correo.com" in data["email"]
    assert "password" not in data


def test_registro_correo_duplicado(test_app, test_database, add_user):
    add_user("test", "test@test.com", "test")
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(
            {"username": "prueba2", "email": "test@test.com", "password": "test"}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert resp.content_type == "application/json"
    assert "El correo ya existe." in data["message"]


@pytest.mark.parametrize(
    "payload",
    [
        [{}],
        [{"email": "nombre@correo.com", "password": "contraseña1"}],
        [{"username": "nombre2", "password": "contraseña2"}],
        [{"email": "nombre@correo.com", "username": "nombre3"}],
    ],
)
def test_registro_usuario_json_no_valido(test_app, test_database, payload):
    client = test_app.test_client()
    resp = client.post(
        f"/auth/register", data=json.dumps(payload), content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert resp.content_type == "application/json"
    assert "Input payload validation failed" in data["message"]


def test_registro_usuario_valido(test_app, test_database, add_user):
    add_user("test3", "test3@test.com", "test")
    client = test_app.test_client()
    resp = client.post(
        "/auth/login",
        data=json.dumps({"email": "test3@test.com", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert data["access_token"]
    assert data["refresh_token"]


def test_usuario_no_registrado(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/auth/login",
        data=json.dumps({"email": "testnotreal@test.com", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert resp.content_type == "application/json"
    assert "El usuario no existe." in data["message"]


def test_token_refresco_valido(test_app, test_database, add_user):
    add_user("test4", "test4@test.com", "test")
    client = test_app.test_client()
    # login de usario
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test4@test.com", "password": "test"}),
        content_type="application/json",
    )
    # Token de refresco válido
    data = json.loads(resp_login.data.decode())
    refresh_token = json.loads(resp_login.data.decode())["refresh_token"]
    resp = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": refresh_token}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert data["access_token"]
    assert data["refresh_token"]


def test_token_caducado(test_app, test_database, add_user):
    add_user("test5", "test5@test.com", "test")
    test_app.config["REFRESH_TOKEN_EXPIRATION"] = -1
    client = test_app.test_client()
    # user login
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test5@test.com", "password": "test"}),
        content_type="application/json",
    )
    # invalid token refresh
    refresh_token = json.loads(resp_login.data.decode())["refresh_token"]
    resp = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": refresh_token}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert resp.content_type == "application/json"
    assert "Firma caducada, vuelva a autenticarse." in data["message"]


def test_token_refresco_invalido(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": "Invalid"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert resp.content_type == "application/json"
    assert "Token no válido, vuelva a autenticarse." in data["message"]


def test_estado_usuario(test_app, test_database, add_user):
    add_user("test6", "test6@test.com", "test")
    client = test_app.test_client()
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test6@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["access_token"]
    resp = client.get(
        "/auth/status",
        headers={"Authorization": f"{token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert "test6" in data["name"]
    assert "test6@test.com" in data["email"]
    assert "password" not in data


def test_estado_usuario_invalido(test_app, test_database):
    client = test_app.test_client()
    resp = client.get(
        "/auth/status",
        headers={"Authorization": "Bearer invalid"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert resp.content_type == "application/json"
    assert "Token no válido" in data["message"]


