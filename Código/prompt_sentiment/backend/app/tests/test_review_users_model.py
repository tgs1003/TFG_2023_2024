from app.api.models.review_users import ReviewUser

def test_create_review_user(add_review_user):
    id = "abc1"
    name = "Usuario abc1"
    review_user = add_review_user(id, name)
    assert review_user.id == id
    assert review_user.name == name