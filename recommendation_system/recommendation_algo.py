import sys
sys.path.append("..")
import os
from recommendation_system.setup_database import DatabaseServices

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '..', 'services', 'recommendation_engine.db')
db_path = os.path.normpath(db_path)

# Initialize database services and other necessary services

class RecommendationSystem:
    def __init__(self):
        self.database = DatabaseServices(db_path)

    def get_meal_type_items(self, item_id):
        query = """SELECT  *
        FROM item_audit
        WHERE item_id = ?"""
        result = self.database.execute(query, (item_id,))
        result = self.database.fetchone()
        return result[0] if result else 0

    def get_item_cooked_number_of_times(self, item_id):
        query = """SELECT  COUNT(*) as cooked_number_of_times 
        FROM item_audit
        WHERE item_id = ?"""
        result = self.database.fetchone(query, (item_id,))
        item_count = result[0] if result else 0
        return item_count

    def get_total_item_count(self):
        query = """SELECT COUNT(*) as total_count 
                   FROM item_audit"""
        result = self.database.fetchone(query)
        total_count = result[0] if result else 0
        return total_count

    def get_item_percentage_of_total(self, item_id):
        item_count = self.get_item_cooked_number_of_times(item_id)
        total_count = self.get_total_item_count()
        if total_count == 0:
            return 0
        item_cooked_ratio = (item_count / total_count)
        return item_cooked_ratio

    def fetch_items_with_feedback(self, meal_type_id, target_date):
        query = """
        SELECT item.id, item.name, item.meal_type_id, 
               AVG(feedback.rating) as avg_rating, 
               AVG(feedback.sentiment_score) as avg_sentiment_score, 
               feedback.date
        FROM voted_item
        INNER JOIN item ON item.id = voted_item.item_id
        LEFT JOIN feedback ON feedback.item_id = voted_item.item_id
        WHERE item.meal_type_id = ?
        AND feedback.date = ?
        GROUP BY item.id, item.name, item.meal_type_id, feedback.date
        """
        result = self.database.fetchall(query, (meal_type_id, target_date))
        return result


def get_recommendation(meal_type_id, target_date):
    item_scores = []

    rec_system = RecommendationSystem()
    
    items_with_feedback = rec_system.fetch_items_with_feedback(meal_type_id, target_date)

    for item in items_with_feedback:
        item_id = item[0]
        item_name = item[1]
        rating = item[3] if item[3] is not None else 0
        sentiment_score = item[4] if item[4] is not None else 0
        
        cooked_percentage = rec_system.get_item_percentage_of_total(item_id)
        final_score = (rating + sentiment_score + cooked_percentage) / 3
        
        item_scores.append((item_name, final_score))

    # Sort items by score in descending order
    item_scores.sort(key=lambda x: x[1], reverse=True)

    return item_scores[:5]

meal_type_id = 1
target_date = "2024-06-21 14:30:00"
recommendations = get_recommendation(meal_type_id, target_date)
print("RECOMMENDATIONS ------------", recommendations)
