from app import db

class Product(db.Model):
    '''
    Modelo de base de datos para la entidad Product
    @author: Teodoro Ricardo García Sánchez
    '''
    __tablename__ = 'products'
    productId = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    reviews = db.relationship("Review", back_populates="product")
