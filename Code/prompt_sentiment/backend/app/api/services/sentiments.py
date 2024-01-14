from app import db
from app.api.models.sentiments import Sentiment
from app.api.models.reviews import Review
from sqlalchemy import func


def get_all_sentiments():
    '''
    Devuelve todos los sentimientos de la base de datos
    '''
    return Sentiment.query.all()

def get_sentiments_by_dataset_id(dataset_id):
    '''
    Devuelve los sentimientos de un dataset
    '''
    query = db.session.query(Sentiment)
    query = query.join(Review, Review.id == Sentiment.review_id)
    query = query.filter(Review.dataset_id == dataset_id)
    return query.all()

def count_sentiments_by_dataset_id(dataset_id):
    '''
    Cuenta el número de sentimientos de un dataset
    '''
    query = db.session.query(Sentiment)
    query = query.join(Review, Review.id == Sentiment.review_id)
    query = query.filter(Review.dataset_id == dataset_id)
    query = query.with_entities(func.count())
    return query.scalar()

def get_sentiment_by_id(id):
    '''
    Devuelve un sentimiento concreto
    '''
    return Sentiment.query.filter_by(id = id).first()

def get_old_sentiment(review_id, model):
    '''
    Devuelve un sentimiento anterior
    '''
    return Sentiment.query.filter_by(review_id=review_id,
                                     model=model).first()

def add_sentiment(review_id, process_time, correct, model, stars = 0, sentiment="", anger=False, source="", tokens=0):
    '''
    Agrega un sentimiento
    '''
    sentiment = Sentiment(review_id=review_id, stars=stars,
                          sentiment=sentiment,
                          anger=anger, source=source,
                          model=model, correct=correct,
                          process_time = process_time, tokens=tokens)
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
