from app import db
from app.api.models.review_users import ReviewUser
from app.api.models.sentiments import Sentiment
from app.api.models.reviews import Review
from sqlalchemy import func, and_

def get_all_reviewusers():
    '''
    Devuelve todos los usuarios de las reseñas
    '''
    return ReviewUser.query.all()

def get_reviewusers_with_sentiments():
    '''
    Devuelve los usuarios que tienen sentimientos
    '''
    query2 = db.session.query(Review.reviewerId).group_by(Review.reviewerId).having(func.count(Review.id)>8).subquery()
    query = db.session.query(ReviewUser)
    query = query.join(Review, Review.reviewerId == ReviewUser.id)
    query = query.join(Sentiment, Sentiment.reviewId == Review.id)
    query = query.filter(
        and_(
            Sentiment.correct == True,
            Review.reviewerId.in_(query2)
            )
        )
    return query.all()

def get_reviewuser_by_id(reviewuser_id):
    '''
    Devuelve un usuario por Id
    '''
    return ReviewUser.query.filter_by(id=reviewuser_id).first()

def add_reviewuser(reviewuser_id, name):
    '''
    Agrega un usuario
    '''
    reviewuser = ReviewUser(id=reviewuser_id, name=name)
    db.session.add(reviewuser)
    db.session.commit()
    return reviewuser

def update_reviewuser(reviewuser, name):
    '''
    Actualiza un usuario
    '''
    reviewuser.name = name
    db.session.commit()
    return reviewuser
    
def delete_reviewuser(reviewuser):
    '''
    Borra un usuario
    '''
    db.session.delete(reviewuser)
    db.session.commit()
    return reviewuser