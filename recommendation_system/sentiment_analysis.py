# from textblob import TextBlob

# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from flair.models import TextClassifier
# from flair.data import Sentence
# from numpy import triu



# sentence = TextBlob("The food was salty.")
# print("text blob --------",sentence.sentiment)




# # Initialize the VADER sentiment intensity analyzer
# analyzer = SentimentIntensityAnalyzer()

# # Define a list of sentences for analysis
# scores = analyzer.polarity_scores("The food was salty.")
   
# print(f"Scores after vader-------: {scores}\n")


from flair.models import TextClassifier
from flair.data import Sentence

# Load the pre-trained sentiment analysis model
classifier = TextClassifier.load('en-sentiment')

# Create a sentence object
sentence = Sentence('Great loved the taste.')

# Predict the sentiment
classifier.predict(sentence)

# Output the result
for label in sentence.labels:
    print(label)
    print(label.value)
    print(label.score)
