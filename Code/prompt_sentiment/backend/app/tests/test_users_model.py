from app.api.models.users import User
from app.api.services.tokens import decode_token, encode_token


def test_passwords_are_random(test_app, test_database, add_user):
    user_one = add_user("justatest", "test@test.com", "greaterthaneight")
    user_two = add_user("justatest2", "test@test2.com", "greaterthaneight")
    assert user_one.password != user_two.password


def test_encode_token(test_app, test_database, add_user):
    user = add_user("justatest3", "test@test3.com", "test")
    token = encode_token(user.id, "access")
    assert isinstance(token, str)


def test_decode_token(test_app, test_database, add_user):
    user = add_user("justatest4", "test@test4.com", "test")
    token = encode_token(user.id, "access")
    assert isinstance(token, str)
    assert decode_token(token) == user.id