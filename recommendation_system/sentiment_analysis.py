from flair.models import TextClassifier
from flair.data import Sentence

# Load the pre-trained sentiment analysis model once
classifier = TextClassifier.load('en-sentiment')

def get_sentiment_score(comment):
    # Create a sentence object
    review = Sentence(comment)
    
    # Predict the sentiment
    classifier.predict(review)
    
    # Extract the score
    for label in review.labels:
        return label.score
# Example usage
result = get_sentiment_score('Great loved the taste.')
print(type(result))
