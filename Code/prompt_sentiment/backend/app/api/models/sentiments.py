from sqlalchemy.sql import func
from app import db

class Sentiment(db.Model):
    '''
    Modelo de base de datos para la entidad Sentiment
    @author: Teodoro Ricardo García Sánchez
    '''
    __tablename__ = 'sentiments'
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    review_id = db.Column(db.Integer, db.ForeignKey("reviews.id", ondelete='CASCADE'), nullable=False)
    stars = db.Column(db.Integer)
    sentiment = db.Column(db.String)
    anger = db.Column(db.Boolean)
    source = db.Column(db.String)
    model = db.Column(db.String)
    creation_date = db.Column(db.DateTime, server_default=func.now())
    correct = db.Column(db.Boolean)
    process_time = db.Column(db.Integer)
    tokens = db.Column(db.Integer)
    reviews = db.relationship("Review", back_populates="sentiment")

    def __init__(self, review_id="", stars="", sentiment="",
                 anger = "", source="", model="",
                 correct = "", process_time = "", tokens = ""):
        self.review_id = review_id
        self.stars = stars
        self.sentiment = sentiment
        self.anger = anger
        self.source = source
        self.model = model
        self.correct = correct
        self.process_time = process_time
        self.tokens = tokens