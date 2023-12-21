from datetime import datetime
from app.api.models.sentiments import Sentiment

def test_create_sentiment(add_sentiment):
    review_id = 1
    stars = 3
    sentiment = "Positive"
    anger = False
    item = "Boots"
    brand = "Dr.Martens"
    language = "en"
    source = ""
    model = ""
    creation_date = datetime.now()
    correct = True
    process_time = 2
    tokens = 2000    
    sentiment = add_sentiment(review_id, stars, 
                              sentiment, anger, 
                              item, brand, 
                              language, source, 
                              model, creation_date, 
                              correct, process_time, tokens)
    assert sentiment.review_id == review_id
    assert sentiment.stars == stars
    assert sentiment.sentiment == sentiment
    assert sentiment.anger == anger
    assert sentiment.item == item
    assert sentiment.brand == brand
    assert sentiment.language == language
    assert sentiment.source == source
    assert sentiment.creation_date < datetime.now()
    assert sentiment.correct == True
    assert sentiment.process_time == 2
    assert sentiment.tokens == 2000