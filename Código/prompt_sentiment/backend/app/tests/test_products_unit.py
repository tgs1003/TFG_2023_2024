import json
import pytest
import app.api.views.products

def test_add_product(test_app, monkeypatch):
    def mock_get_product_by_id(productId):
        return None
    def mock_add_product(productId, title):
        return True
    
    monkeypatch.setattr(app.api.views.products, "get_product_by_id", mock_get_product_by_id)
    monkeypatch.setattr(app.api.views.products, "add_product", mock_add_product)
    
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

def test_add_product_duplicado(test_app, monkeypatch):
    def mock_get_product_by_id(productId):
        return True
    def mock_add_product(productId, title):
        return True
    
    monkeypatch.setattr(app.api.views.products, "get_product_by_id", mock_get_product_by_id)
    monkeypatch.setattr(app.api.views.products, "add_product", mock_add_product)
    
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

def test_add_product_faltan_datos(test_app, monkeypatch):
    def mock_get_product_by_id(productId):
        return None
    def mock_add_product(productId, title):
        return True
    
    monkeypatch.setattr(app.api.views.products, "get_product_by_id", mock_get_product_by_id)
    monkeypatch.setattr(app.api.views.products, "add_product", mock_add_product)
    
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

def test_get_product_no_existe(test_app, monkeypatch):
    def mock_get_product_by_id(product_id):
        return None
    monkeypatch.setattr(app.api.views.products, "get_product_by_id", mock_get_product_by_id)
    
    client = test_app.test_client()
    resp = client.get("/products/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El producto 999 no existe" in data["message"]

def test_delete_product_incorrect_id(test_app, monkeypatch):
    def mock_get_dataset_by_id(dataset_id):
        return None
    
    monkeypatch.setattr(app.api.views.products, "get_products_by_id", mock_get_dataset_by_id)
    
    client = test_app.test_client()
    resp = client.delete("/products/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "El producto 999 no existe" in data["message"]

def test_update_product_correct(test_app, monkeypatch):
    def mock_get_product_by_id(productId):
        return True
    def mock_add_product(productId, title):
        return True
    
    monkeypatch.setattr(app.api.views.products, "get_product_by_id", mock_get_product_by_id)
    monkeypatch.setattr(app.api.views.products, "add_product", mock_add_product)
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

def test_update_product_incorrect_request(test_app, product_id, payload, status_code, message, monkeypatch):
    def mock_get_product_by_id(productId):
        return None
    
    
    monkeypatch.setattr(app.api.views.products, "get_product_by_id", mock_get_product_by_id)
    
    client = test_app.test_client()
    resp = client.put(f"/products/{product_id}", data=json.dumps(payload),content_type="application/json")

    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
