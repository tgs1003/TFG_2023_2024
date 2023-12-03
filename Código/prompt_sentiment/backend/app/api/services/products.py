from app import db
from app.api.models.products import Product

def get_all_products():
    '''
    Devuelve todos los productos
    '''
    return Product.query.all()

def get_product_by_id(productId):
    '''
    Devuelve un producto
    '''
    return Product.query.filter_by(productId = productId).first()

def add_product(productId, title):
    '''
    Agrega un producto
    '''
    product = Product(productId = productId, title = title)
    db.session.add(product)
    db.session.commit()
    return product

def update_product(product, title):
    '''
    Actualiza un producto
    '''
    product.title = title
    db.session.commit()
    return product

def delete_product(product):
    '''
    Borra un producto
    '''
    db.session.delete(product)
    db.session.commit()
    return product