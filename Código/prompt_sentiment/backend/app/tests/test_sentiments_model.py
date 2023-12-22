from datetime import datetime
from app.api.models.sentiments import Sentiment

def test_create_sentiment(test_app, test_database, add_sentiment, add_review, add_dataset, add_user):
    user1 = add_user("justatest1234", "test_review1@test123.com", "greaterthaneight", "Gestor")
    dataset1 = add_dataset(name = "dataset_name", type = "dataset_type", 
                          config = "dataset_config", owner = user1.id)
    review1 = add_review(dataset_id = dataset1.id,  
                        review_text="review_text",
                        review_time = datetime.now().isoformat(),
                        original_stars=0)
    
    stars = 3
    sentiment = "Positive"
    anger = False
    source = ""
    model = ""
    correct = True
    process_time = 2
    tokens = 2000    
    sentiment1 = add_sentiment(review1.id, stars, 
                              sentiment, anger, 
                            source, 
                              model, 
                              correct, process_time, tokens)
    assert sentiment1.review_id == review1.id
    assert sentiment1.stars == stars
    assert sentiment1.sentiment == sentiment
    assert sentiment1.anger == anger
    assert sentiment1.source == source
    assert sentiment1.creation_date < datetime.now()
    assert sentiment1.correct == True
    assert sentiment1.process_time == 2
    assert sentiment1.tokens == 2000