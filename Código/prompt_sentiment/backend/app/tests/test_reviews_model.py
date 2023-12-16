from datetime import datetime
from app.api.models.sentiments import Sentiment

def test_create_review(add_review):
    
    originalId='or_id1'
    productId = 'product1'
    reviewText = 'ReviewText1234'
    reviewTime = datetime.now()
    reviewerId = 1
    originalStars = 5

    review = add_review(originalId=originalId, 
                        productId=productId, 
                        reviewText=reviewText,
                        reviewTime = reviewTime,
                        reviewerId = reviewerId,
                        originalStars=originalStars)
    
    assert review.originalId == originalId
    assert review.productId == productId
    assert review.reviewText == reviewText
    assert review.reviewTime == reviewTime
    assert review.reviewerId == reviewerId
    assert review.originalStars == originalStars
