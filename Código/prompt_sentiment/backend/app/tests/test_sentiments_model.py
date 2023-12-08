from datetime import datetime
from app.api.models.sentiments import Sentiment

def test_create_sentiment(add_sentiment):
    reviewId = 1
    stars = 3
    sentiment = "Positive"
    anger = False
    item = "Boots"
    brand = "Dr.Martens"
    language = "en"
    source = ""
    model = ""
    creationDate = datetime.now()
    correct = True
    processTime = 2
    tokens = 2000    
    sentiment = add_sentiment(reviewId, stars, 
                              sentiment, anger, 
                              item, brand, 
                              language, source, 
                              model, creationDate, 
                              correct, processTime, tokens)
    assert sentiment.reviewId == reviewId
    assert sentiment.stars == stars
    assert sentiment.sentiment == sentiment
    assert sentiment.anger == anger
    assert sentiment.item == item
    assert sentiment.brand == brand
    assert sentiment.language == language
    assert sentiment.source == source
    assert sentiment.creationDate < datetime.now()
    assert sentiment.correct == True
    assert sentiment.processTime == 2
    assert sentiment.tokens == 2000