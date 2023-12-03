from app import db

class ReviewUser(db.Model):
    '''
    Modelo de base de datos para la entidad ReviewUser
    @author: Teodoro Ricardo García Sánchez
    '''
    __tablename__ = 'review_users'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    reviews = db.relationship("Review", back_populates="reviewer")
