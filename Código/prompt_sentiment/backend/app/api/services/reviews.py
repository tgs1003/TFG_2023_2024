import logging
from app import db
from app.api.models.reviews import Review

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

def count_reviews_by_dataset_id(datasetId):
    '''
    Cuenta las reseñas de un dataset
    '''
    return Review.query.filter_by(datasetId = datasetId).count()

def get_review_by_id(review_id):
    '''
    Busca una reseña por Id
    '''
    return Review.query.filter_by(id = review_id).first()

def get_review_by_dataset_id_and_review_id(dataset_id, review_id):
    '''
    Busca una reseña por Id
    '''
    return Review.query.filter_by(original_id = review_id, dataset_id = dataset_id).first()

def add_review(dataset_id, review_text, review_time, stars):
    '''
    Agrega una reseña
    '''
    review = Review(dataset_id = dataset_id,
                    review_text = review_text, 
                    review_time = review_time, 
                    original_stars = stars)
    db.session.add(review)
    db.session.commit()
    return review

def update_review(review, review_text):
    '''
    Actualiza una reseña
    '''
    review.review_text = review_text
    db.session.commit()
    return review

def delete_review(review):
    '''
    Borra una reseña
    '''
    db.session.delete(review)
    db.session.commit()
    return review

