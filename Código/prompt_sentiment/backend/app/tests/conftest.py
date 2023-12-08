import pytest
from app import create_app, db
from app.api.models.users import User
from app.api.models.datasets import Dataset
from app.api.models.products import Product
from app.api.models.review_users import ReviewUser
from app.api.models.reviews import Review
from app.api.models.sentiments import Sentiment


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("app.config.TestingConfig")
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def test_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="module")
def add_user():
    def _add_user(username, email, password):
        user = User(name=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    return _add_user

@pytest.fixture(scope="module")
def add_dataset():
    def _add_dataset(dataset_name, dataset_type, dataset_payload):
        dataset = Dataset(name=dataset_name, type=dataset_type, payload=dataset_payload)
        db.session.add(dataset)
        db.session.commit()
        return dataset
    return _add_dataset

@pytest.fixture(scope="module")
def add_product():
    def _add_product(product_id, title):
        product = Product(productId = product_id, title = title)
        db.session.add(product)
        db.session.commit()
        return product
    return _add_product

@pytest.fixture(scope="module")
def add_review_user():
    def _add_review_user(id, name):
        review_user = ReviewUser(id = id, name = name)
        db.session.add(review_user)
        db.session.commit()
        return review_user
    return _add_review_user

@pytest.fixture(scope="module")
def add_review():
    def _add_review(dataset_id, original_id, product_id, review_text, review_time, reviewer_id, original_stars):
        review = Review(datasetId = dataset_id, originalId = original_id, 
                        productId = product_id, reviewText = review_text, 
                        reviewTime = review_time, reviewerId=reviewer_id, 
                        originalStars=original_stars)
        db.session.add(review)
        db.session.commit()
        return review
    return _add_review

@pytest.fixture(scope="module")
def add_sentiment():
    def _add_sentiment(reviewId, stars, sentiment, anger, item, brand, language, source, model, creationDate, correct, processTime, tokens):
        sentiment = Sentiment(reviewId, stars, sentiment, anger, item, brand, language, source, model, creationDate, correct, processTime, tokens)
        db.session.add(sentiment)
        db.session.commit()
        return sentiment
    return _add_sentiment
