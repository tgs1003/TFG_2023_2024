from app import db
from app.api.models.sentiments import Sentiment
from app.api.models.reviews import Review
from sqlalchemy import exists, func, and_


def get_all_sentiments():
    '''
    Devuelve todos los sentimientos de la base de datos
    '''
    return Sentiment.query.all()

def get_sentiments_by_datasetId(datasetId):
    '''
    Devuelve los sentimientos de un dataset
    '''
    return db.session.query(Sentiment).filter(
        exists().where(Sentiment.reviewId==Review.id and Review.datasetId == datasetId)
        ).all()

def get_sentiments_by_reviewuser_id_and_dataset_id(review_user_id, dataset_id):
    '''
    Devuelve los sentimientos de un usuario
    '''
    query = db.session.query(Sentiment)
    query = query.join(Review, Review.id == Sentiment.reviewId)
    query = query.filter(Review.reviewerId == review_user_id, Review.datasetId == dataset_id, Sentiment.correct)
    query = query.with_entities(Review.datasetId, Review.id, Sentiment.sentiment, 
                                Review.originalStars, Review.reviewText, 
                                Sentiment.stars,Sentiment.processTime, 
                                Sentiment.tokens, Sentiment.model, Review.productId)
    return query.all()

def get_sentiments_by_reviewuser_id(review_user_id):
    '''
    Devuelve los sentimientos de un usuario
    '''
    query = db.session.query(Sentiment)
    query = query.join(Review, Review.id == Sentiment.reviewId)
    query = query.filter(Review.reviewerId == review_user_id)
    query = query.with_entities(Review.datasetId, Review.id, Sentiment.sentiment, 
                                Review.originalStars, Review.reviewText, 
                                Sentiment.stars,Sentiment.processTime, 
                                Sentiment.tokens, Sentiment.model, Review.productId)
    return query.all()

def get_sentiments_by_product_id_and_dataset_id(product_id, dataset_id):
    '''
    Devuelve los sentimientos de un usuario
    '''
    query = db.session.query(Sentiment)
    query = query.join(Review, Review.id == Sentiment.reviewId)
    query = query.filter(Review.productId == product_id, Review.datasetId == dataset_id, Sentiment.correct)
    query = query.with_entities(Review.datasetId, Review.id, Sentiment.sentiment, 
                                Review.originalStars, Review.reviewText, 
                                Sentiment.stars,Sentiment.processTime, 
                                Sentiment.tokens, Sentiment.model, Review.productId)
    return query.all()
    
def get_sentiments_by_product_id(product_id):
    '''
    Devuelve los sentimientos de un producto
    '''
    return db.session.query(Sentiment).filter(
        and_(
            exists().where(Sentiment.reviewId==Review.id and Review.productId == product_id), 
            Sentiment.correct==True
            )).all()

def count_sentiments_by_datasetId(datasetId):
    '''
    Cuenta el número de sentimientos de un dataset
    '''
    query = db.session.query(Sentiment)
    query = query.join(Review, Review.id == Sentiment.reviewId)
    query = query.filter(Review.datasetId == datasetId)
    # Note: important to place `with_entities` after the join
    query = query.with_entities(func.count())    
    return query.scalar()
    
def get_sentiment_by_id(id):
    '''
    Devuelve un sentimiento concreto
    '''
    return Sentiment.query.filter_by(id=id).first()

def get_old_sentiment(reviewId, model):
    '''
    Devuelve un sentimiento anterior
    '''
    return Sentiment.query.filter_by(reviewId=reviewId, model=model).first()

def add_sentiment(reviewId, processTime, correct, model, stars=0, sentiment="", anger=False, item="", brand="", language="", source="", tokens=0):
    '''
    Agrega un sentimiento
    '''
    sentiment = Sentiment(reviewId=reviewId, stars=stars, sentiment=sentiment, 
                        anger=anger, item=item, brand=brand, language=language, source=source, 
                        model=model, correct=correct, processTime=processTime, tokens=tokens)
    db.session.add(sentiment)
    db.session.commit()
    return sentiment

def update_sentiment(sentiment, correct):
    '''
    Actualiza un sentimiento
    '''
    sentiment.correct = correct
    db.session.commit()
    return sentiment

def delete_sentiment(sentiment):
    '''
    Borra un sentimiento
    '''
    db.session.delete(sentiment)
    db.session.commit()
    return sentiment
