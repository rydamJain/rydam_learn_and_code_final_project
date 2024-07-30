from flair.models import TextClassifier
from flair.data import Sentence

# Load the pre-trained sentiment analysis model once
classifier = TextClassifier.load('en-sentiment')

def get_sentiment_score(comment):
    # Create a sentence object
    review = Sentence(comment)
    
    # Predict the sentiment
    classifier.predict(review)
    
    # Extract the label and the score
    for label in review.labels:
        sentiment = label.value
        score = label.score
        if sentiment == 'NEGATIVE':
            score = 1 - score
        return score

