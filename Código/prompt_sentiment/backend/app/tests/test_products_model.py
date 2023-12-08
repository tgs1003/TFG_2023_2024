from app.api.models.products import Product

def test_create_product(add_product):
    product_id = "abc1"
    product_name = "Producto abc1"
    product = add_product(product_id, product_name)
    assert product.productId == product_id
    assert product.title == product_name