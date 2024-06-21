import sys
import os
sys.path.append("..")
import os
from setup_database import DatabaseServices
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '..', 'services', 'recommendation_engine.db')
db_path = os.path.normpath(db_path)

# Initialize database services and other necessary services

class RecommendationSystem:
    def __init__(self):
        self.database = DatabaseServices(db_path)

    def get_item_cooked_number_of_times(self, item_id):
        query = "SELECT cooked_number_of_times FROM item_audit WHERE item_id = ?"
        result = self.database.execute(query, (item_id,))
        row = result.fetchone()
        return row[0] if row else 0

    def fetch_items_with_feedback(self, meal_type_id, target_date):
        query = """
            SELECT items.id, items.name, items.meal_type_id, feedback.rating, feedback.sentiment_score, feedback.date
            FROM voted_items
            INNER JOIN items ON items.id = voted_items.item_id
            LEFT JOIN feedback ON feedback.item_id = voted_items.item_id
            WHERE voted_items.is_voted = 1
            AND items.meal_type_id = ?
            AND feedback.date = ?
        """
        result = self.database.execute(query, (meal_type_id, target_date))
        return result.fetchall()

def get_recommendation(meal_type_id, target_date):
    item_scores = []

    rec_system = RecommendationSystem()
    
    items_with_feedback = rec_system.fetch_items_with_feedback(meal_type_id, target_date)

    for item in items_with_feedback:
        item_id = item[0]
        item_name = item[1]
        meal_type_id = item[2]
        rating = item[3]
        sentiment_score = item[4]
        feedback_date = item[5] if item[5] else None
        
        cooked_number_of_times = rec_system.get_item_cooked_number_of_times(item_id)

        if feedback_date == target_date:
            final_score = (rating + sentiment_score + cooked_number_of_times) / 3
            item_scores.append((item_name, final_score))

    return sorted(item_scores, key=lambda x: x[1], reverse=True)[:3]



meal_type_id = 2
target_date = "2024-06-21 14:30:00"
recommendations = get_recommendation(meal_type_id, target_date)

