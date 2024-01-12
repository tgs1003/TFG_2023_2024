from app import db

class Review(db.Model):
    '''
    Modelo de base de datos para la entidad Review
    @author: Teodoro Ricardo García Sánchez
    '''
    __tablename__ = 'reviews'
    dataset_id = db.Column(db.Integer, db.ForeignKey("datasets.id", ondelete='CASCADE'), nullable=False)
    id = db.Column(db.Integer,primary_key=True, autoincrement="auto")
    review_text = db.Column(db.String)
    review_time = db.Column(db.DateTime)
    original_stars = db.Column(db.Integer)
    sentiment = db.relationship("Sentiment", back_populates="reviews", passive_deletes=True)
    
    def __init__(self, dataset_id="", review_text="", review_time="", original_stars = ""):
        self.dataset_id = dataset_id
        self.review_text = review_text
        self.review_time = review_time
        self.original_stars = original_stars