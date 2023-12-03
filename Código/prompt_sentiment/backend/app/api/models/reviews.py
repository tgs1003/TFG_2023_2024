from app import db

class Review(db.Model):
    '''
    Modelo de base de datos para la entidad Review
    @author: Teodoro Ricardo García Sánchez
    '''
    __tablename__ = 'reviews'
    datasetId = db.Column(db.Integer, db.ForeignKey("datasets.id"), nullable=False)
    id = db.Column(db.Integer,primary_key=True, autoincrement="auto")
    originalId = db.Column(db.String)
    productId = db.Column(db.String, db.ForeignKey("products.productId"), nullable=False)
    reviewText = db.Column(db.String)
    reviewTime = db.Column(db.DateTime)
    reviewerId = db.Column(db.String, db.ForeignKey("review_users.id"), nullable=False)
    originalStars = db.Column(db.Integer)
    reviewer= db.relationship("ReviewUser", back_populates="reviews")
    sentiment = db.relationship("Sentiment", back_populates="reviews")
    product = db.relationship("Product", back_populates="reviews")
    
