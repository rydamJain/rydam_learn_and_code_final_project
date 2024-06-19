from flair.models import TextClassifier
from flair.data import Sentence
from datetime import datetime

# Load the pre-trained sentiment analysis model
classifier = TextClassifier.load('en-sentiment')

# Extended sample data with vegetarian feedback from employees only
data = [
    {
        
        "item": {
            id,price
            "name": "Aloo Paratha",
            "category": "Breakfast",
            "cooked_number_of_times": 10,
            "feedback": [
                {
                    "user": "employee123",
                    "rating": 4.5,
                    "comment": "Delicious and perfectly cooked!",
                    "timestamp": "2024-06-01T12:34:56Z"
                },
                {
                    "user": "employee456",
                    "rating": 4.0,
                    "comment": "Great taste but a bit too fatty for me.",
                    "timestamp": "2024-06-01T08:20:43Z"
                }
            ]
        }
    },
    {
        "roles": [
            {"role_id": 1, "role_name": "admin"},
            {"role_id": 2, "role_name": "employee"}
        ],
        "role_mapping": {
            "1": "Can manage food items and view all feedback",
            "2": "Can assist in managing food items and provide feedback"
        },
        "item": {
            "name": "Pav Bhaji",
            "category": "Breakfast",
            "cooked_number_of_times": 15,
            "feedback": [
                {
                    "user": "employee789",
                    "rating": 5.0,
                    "comment": "Fresh and crispy, loved the dressing!",
                    "timestamp": "2024-06-01T14:56:30Z"
                },
                {
                    "user": "employee012",
                    "rating": 4.5,
                    "comment": "Very tasty, could use a bit more vegetables.",
                    "timestamp": "2024-06-01T09:15:21Z"
                }
            ]
        }
    },
    {
        "roles": [
            {"role_id": 2, "role_name": "employee"},
            {"role_id": 3, "role_name": "chef"}
        ],
        "role_mapping": {
            "2": "Can assist in managing food items and provide feedback",
            "3": "Can create and update recipes and send notifications"
        },
        "item": {
            "name": "Paneer Butter Masala",
            "category": "Lunch",
            "cooked_number_of_times": 20,
            "feedback": [
                {
                    "user": "employee345",
                    "rating": 4.8,
                    "comment": "Rich in protein, a health conscious person's dream!",
                    "timestamp": "2024-06-01T11:22:33Z"
                },
                {
                    "user": "employee678",
                    "rating": 4.0,
                    "comment": "Great flavor but a bit too sweet.",
                    "timestamp": "2024-06-01T15:48:59Z"
                }
            ]
        }
    },
    {
        "roles": [
            {"role_id": 2, "role_name": "employee"},
            {"role_id": 3, "role_name": "chef"}
        ],
        "role_mapping": {
            "2": "Can assist in managing food items and provide feedback",
            "3": "Can create and update recipes and send notifications"
        },
        "item": {
            "name": "Vegetable Biryani",
            "category": "Lunch",
            "cooked_number_of_times": 25,
            "feedback": [
                {
                    "user": "employee890",
                    "rating": 5.0,
                    "comment": "Perfect blend of spices!",
                    "timestamp": "2024-06-01T12:10:22Z"
                },
                {
                    "user": "employee123",
                    "rating": 4.7,
                    "comment": "Really enjoyed it!",
                    "timestamp": "2024-06-01T14:32:10Z"
                }
            ]
        }
    },
    {
        "roles": [
            {"role_id": 2, "role_name": "employee"},
            {"role_id": 3, "role_name": "chef"}
        ],
        "role_mapping": {
            "2": "Can assist in managing food items and provide feedback",
            "3": "Can create and update recipes and send notifications"
        },
        "item": {
            "name": "Veg Biryani",
            "category": "Dinner",
            "cooked_number_of_times": 30,
            "feedback": [
                {
                    "user": "employee456",
                    "rating": 4.9,
                    "comment": "Aromatic and flavorful!",
                    "timestamp": "2024-06-01T19:45:56Z"
                },
                {
                    "user": "employee789",
                    "rating": 4.5,
                    "comment": "Really good, could use a bit more spice.",
                    "timestamp": "2024-06-01T20:30:21Z"
                }
            ]
        }
    },
    {
        "roles": [
            {"role_id": 2, "role_name": "employee"},
            {"role_id": 3, "role_name": "chef"}
        ],
        "role_mapping": {
            "2": "Can assist in managing food items and provide feedback",
            "3": "Can create and update recipes and send notifications"
        ],
        "item": {
            "name": "Paneer Tikka",
            "category": "Dinner",
            "cooked_number_of_times": 22,
            "feedback": [
                {
                    "user": "employee234",
                    "rating": 4.6,
                    "comment": "Fresh and tasty!",
                    "timestamp": "2024-06-01T18:30:11Z"
                },
                {
                    "user": "employee678",
                    "rating": 4.2,
                    "comment": "Nice flavor but a bit too salty.",
                    "timestamp": "2024-06-01T19:15:43Z"
                }
            ]
        }
    }
]

# Function to get average rating, sentiment score, and count for employee feedback by category and date
def analyze_feedback(data, meal_category, target_date):
    target_date = datetime.strptime(target_date, "%Y-%m-%d")
    item_scores = []

    for entry in data:
        item = entry['item']
        item_name = item['name']
        item_category = item['category']
        feedbacks = item['feedback']
        cooked_number_of_times = item['cooked_number_of_times']
        
        if item_category.lower() != meal_category.lower():
            continue

        rating_sum = 0
        rating_count = 0
        sentiment_sum = 0
        sentiment_count = 0
        
        for feedback in feedbacks:
            feedback_date = datetime.strptime(feedback['timestamp'], "%Y-%m-%dT%H:%M:%SZ").date()
            rating = feedback['rating']
            comment = feedback['comment']
            
            # Only consider feedback matching the target date
            if feedback_date == target_date:
                rating_sum += rating
                rating_count += 1
                
                # Sentiment analysis
                sentence = Sentence(comment)
                classifier.predict(sentence)
                for label in sentence.labels:
                    score = label.score if label.value == 'POSITIVE' else -label.score
                    sentiment_sum += score
                    sentiment_count += 1

        if rating_count > 0 and sentiment_count > 0:
            avg_rating = rating_sum / rating_count if rating_count > 0 else 0
            avg_sentiment = sentiment_sum / sentiment_count if sentiment_count > 0 else 0
            final_score = (avg_rating + avg_sentiment + cooked_number_of_times) / 3
            item_scores.append((item_name, final_score))

    return sorted(item_scores, key=lambda x: x[1], reverse=True)

# Specify the meal categories and date for the recommendation
meal_categories = ["Breakfast", "Lunch", "Dinner"]
target_date = "2024-06-01"

# Get the sorted list of items based on the final score for each category
for meal_category in meal_categories:
    print(f"Recommendations for {meal_category} on {target_date}:")
    sorted_items = analyze_feedback(data, meal_category, target_date)
    for item in sorted_items:
        print(f"Item: {item[0]}, Final Score: {item[1]:.2f}")
    print()  # Print a blank line for readability
