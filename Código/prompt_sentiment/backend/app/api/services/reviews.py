import logging
from app import db
from app.api.models.reviews import Review
from sqlalchemy import func, and_, or_

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])


def get_all_reviews():
    '''
    Devuelve todas las reseñas
    '''
    return Review.query.all()

def get_reviews_by_dataset_id(datasetId):
    '''
    Devuelve las reseñas de un dataset
    '''
    logging.debug("Dataset id: " + str(datasetId))
    return Review.query.filter_by(datasetId=datasetId).all()

def get_reviews_by_dataset_id_for_process(datasetId, n_products=13, n_reviewers=8):
    '''
    Devuelve las reseñas que cumplen una serie de requisitos:
        - Que sean de productos con más de n reseñas
        - o que sean de usuarios con más de m reseñas
        - y que pertenezcan a determinado dataset
    '''
    logging.debug("Dataset id: " + str(datasetId))
    query1 = db.session.query(Review.productId).group_by(Review.productId).having(func.count(Review.id)>n_products).subquery()
    query2 = db.session.query(Review.reviewerId).group_by(Review.reviewerId).having(func.count(Review.id)>n_reviewers).subquery()
    query = db.session.query(Review).filter(
        and_(
            Review.datasetId==datasetId,
            or_(
            Review.productId.in_(query1),
            Review.reviewerId.in_(query2)
            )
        ))
    return query.all()

def count_reviews_by_dataset_id(datasetId):
    '''
    Cuenta las reseñas de un dataset
    '''
    return Review.query.filter_by(datasetId = datasetId).count()

def get_review_by_reviewer_and_product(datasetId, reviewer_id, productId):
    '''
    Busca una reseña por usuario y producto
    '''
    return Review.query.filter_by(datasetId = datasetId, reviewerId = reviewer_id , productId = productId).first()

def get_review_by_id(review_id):
    '''
    Busca una reseña por Id
    '''
    return Review.query.filter_by(id=review_id).first()

def get_review_by_dataset_id_and_review_id(dataset_id, review_id):
    '''
    Busca una reseña por Id
    '''
    return Review.query.filter_by(id = review_id, dataset_id = dataset_id).first()

def add_review(datasetId, originalId, productId, reviewText, reviewTime, reviewerId, stars):
    '''
    Agrega una reseña
    '''
    review = Review(datasetId = datasetId,
                    originalId = originalId,
                    productId = productId, 
                    reviewText = reviewText, 
                    reviewTime = reviewTime, 
                    reviewerId = reviewerId,
                    stars = stars)
    db.session.add(review)
    db.session.commit()
    return review

def update_review(review, reviewtext):
    '''
    Actualiza una reseña
    '''
    review.reviewText = reviewtext
    db.session.commit()
    return review

def delete_review(review):
    '''
    Borra una reseña
    '''
    db.session.delete(review)
    db.session.commit()
    return review

