import pytest
from app import create_app, db
from app.api.models.users import User
from app.api.models.datasets import Dataset
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
    def _add_user(username, email, password, rol="Gestor"):
        user = User(name=username,
                    email=email,
                    password=password,
                    rol=rol)
        db.session.add(user)
        db.session.commit()
        return user

    return _add_user

@pytest.fixture(scope="module")
def add_dataset():
    def _add_dataset(name, type, 
                     config, owner):
        dataset = Dataset(name=name,
                          type=type,
                          config=config,
                          owner=owner,
                          status="Creado")
        db.session.add(dataset)
        db.session.commit()
        return dataset
    return _add_dataset


@pytest.fixture(scope="module")
def add_review():
    def _add_review(dataset_id, review_text, review_time, original_stars):
        review = Review(dataset_id = dataset_id,
                        review_text = review_text,
                        review_time = review_time,
                        original_stars=original_stars)
        db.session.add(review)
        db.session.commit()
        return review
    return _add_review

@pytest.fixture(scope="module")
def add_sentiment():
    def _add_sentiment(review_id, stars,
                       sentiment, anger,
                       source, model,
                        correct,
                       process_time, tokens):
        sentiment = Sentiment(review_id, stars,
                              sentiment, anger,
                              source, model, correct,
                              process_time, tokens)
        db.session.add(sentiment)
        db.session.commit()
        return sentiment
    return _add_sentiment
