from sqlalchemy.sql import func
from app import db

class Sentiment(db.Model):
    __tablename__ = 'sentiments'
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    reviewId = db.Column(db.Integer, db.ForeignKey("reviews.id"), nullable=False)
    stars = db.Column(db.Integer)
    sentiment = db.Column(db.String)
    anger = db.Column(db.Boolean)
    item = db.Column(db.String)
    brand = db.Column(db.String)
    language = db.Column(db.String)
    source = db.Column(db.String)
    model = db.Column(db.String)
    creationDate = db.Column(db.DateTime, server_default=func.now())
    correct = db.Column(db.Boolean)
    processTime = db.Column(db.Integer)
    tokens = db.Column(db.Integer)
    reviews = db.relationship("Review", back_populates="sentiment")