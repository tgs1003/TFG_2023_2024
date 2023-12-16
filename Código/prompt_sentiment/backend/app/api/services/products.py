from app import db
from app.api.models.products import Product
from app.api.models.reviews import Review
from app.api.models.sentiments import Sentiment
from sqlalchemy import func, and_


def get_all_products():
    '''
    Devuelve todos los productos
    '''
    return Product.query.all()

def get_products_with_sentiments(dataset_id, min_count=8):
    '''
    Devuelve los productos que tienen sentimientos
    '''
    query2 = db.session.query(Review.productId).group_by(Review.productId).having(func.count(Review.id)>min_count).subquery()
    query = db.session.query(Product)
    query = query.join(Review, Review.productId == Product.productId)
    query = query.join(Sentiment, Sentiment.reviewId == Review.id)
    query = query.filter(
        and_(
            Sentiment.correct == True,
            Review.productId.in_(query2),
            Review.datasetId == dataset_id
            )
        )
    return query.all()

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