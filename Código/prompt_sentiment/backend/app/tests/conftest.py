import pytest
from app import create_app, db
from app.api.models.users import User
from app.api.models.datasets import Dataset


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
