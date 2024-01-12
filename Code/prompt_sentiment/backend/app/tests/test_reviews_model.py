from datetime import datetime
from app.api.models.sentiments import Sentiment

def test_create_review(test_app, test_database, add_review, add_user, add_dataset):
    user1 = add_user("justatest1234", "test123@test123.com", "greaterthaneight", "Gestor")
    dataset1 = add_dataset(name = "dataset_name", type = "dataset_type", 
                          config = "dataset_config", owner = user1.id)
    
    
    review_text = 'ReviewText1234'
    review_time = datetime.now()
    original_stars = 5
    review = add_review(dataset_id = dataset1.id,  
                        review_text=review_text,
                        review_time = review_time,
                        original_stars=original_stars)

    assert review.dataset_id == dataset1.id
    assert review.review_text == review_text
    assert review.review_time == review_time
    assert review.original_stars == original_stars
