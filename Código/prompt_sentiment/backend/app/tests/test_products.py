import json
import pytest

def test_add_product(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/products",
        
        data=json.dumps(
            {
                "product_id": "product1",
                "product_name": "product_name1",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "Se ha añadido el producto: product_name1" in data["message"]

def test_add_product_duplicado(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/products",
        data=json.dumps(
            {
                "product_id": "product1",
                "product_name": "product_name2",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "El producto ya existe." in data["message"]

def test_add_product_faltan_datos(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/products",
        data=json.dumps(
            {
                "product_id": "product4",
                
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]

def test_add_product_correcto(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/products",
        data=json.dumps(
            {
                "product_id": "product3",
                "product_name": "product_name3",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "Se ha añadido el producto: product_name3" in data["message"]
    assert "product_name3" in data["product_name"]
    assert "product3" in data["product_id"]
    
def test_get_product_no_existe(test_app):
    client = test_app.test_client()
    resp = client.get("/products/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El producto 999 no existe" in data["message"]


def test_delete_product(test_app):
    client = test_app.test_client()
    resp = client.get("/products/product1")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "eliminado" in data["message"]

def test_delete_product_incorrect_id(test_app):
    client = test_app.test_client()
    resp = client.get("/products/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El producto 999 no existe" in data["message"]

def test_update_product_correct(test_app):
    client = test_app.test_client()
    resp = client.put(f"/products/product1", data=json.dumps({
                "title": "product_name_modified",
            }),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'Producto product1 actualizado' in data["message"]

@pytest.mark.parametrize(
    "product_id, payload, status_code, message",
    [
        ["product1", {}, 400, "Input payload validation failed"],
        ["product1", {"name": "product1_title"}, 400, "Input payload validation failed"],
        [
            "product999",
            {"title": "product_999"},
            404,
            "El producto 999 no existe",
        ],
    ],
)

def test_update_product_incorrect_request(test_app, product_id, payload, status_code, message):
    client = test_app.test_client()
    resp = client.put(f"/products/{product_id}", data=json.dumps(payload),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
