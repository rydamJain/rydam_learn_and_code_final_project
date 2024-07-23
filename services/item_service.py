import sys
sys.path.append("..")
from recommendation_system.setup_database import DatabaseServices
from datetime import datetime

class ItemServices:
    def __init__(self, database):
        self.database = database

    def insert_into_meal_type(self, meal_types):
        self.database.executemany('''
        INSERT INTO meal_type (id, name) VALUES (?, ?)
        ''', meal_types)

    def get_meal_type_id(self, item_id):
        query = '''SELECT meal_type_id FROM item WHERE item_id = ?'''
        self.database.execute(query, (item_id,))
        result = self.database.fetchone()
        return result[0] if result else None
    
    def insert_into_items(self, items):
        
        self.database.executemany('''
        INSERT INTO item (id, name, price, meal_type_id, availability_status) VALUES (?, ?, ?, ?, ?)
        ''', items)
        print("Item added successfully.")

    def delete_item(self, item_id):
        query = 'DELETE FROM item WHERE id = ?'
        params = (item_id,)
        self.database.execute(query, params)
        print("Item deleted successfully.")

    def update_availability_status(self, item_id, availability_status):
        query = 'UPDATE item SET availability_status = ? WHERE id = ?'
        params = (availability_status, item_id)
        self.database.execute(query, params)
        print("Item availability status updated successfully.")

    def insert_into_voted_items(self, voted_items):
        self.database.executemany('''
        INSERT INTO voted_item (id, item_id, meal_type_id, user_id, is_voted, date) VALUES (?, ?, ?, ?, ?, ?)
        ''', voted_items)

    def insert_into_feedback(self, feedback):
        self.database.executemany('''
        INSERT INTO feedback (id, item_id, user_id, rating, comment,sentiment_score, date) VALUES (?, ?, ?, ?, ?,?, ?)
        ''', feedback)

    def insert_into_item_audit(self, item_audits):
        self.database.executemany('''
        INSERT INTO item_audit (item_id, name, cooked_number_of_times, audit_date) VALUES (?, ?, ?, ?)
        ''', item_audits)

    def insert_into_notification(self, notifications):
        self.database.executemany('''
        INSERT INTO notification (id, user_id, message) VALUES ( ?, ?, ?)
        ''', notifications)
 
    def view_next_day_menu(self, user_id):
        rolled_out_date = str(datetime.today().date()) 
        query = f"""select preference.item_id, preference.item_name from (SELECT rolled_items.*,
                CASE WHEN up.diet = mp.diet THEN 1 ELSE 0 END AS diet_match,
                CASE WHEN up.spice_level = mp.spice_level THEN 1 ELSE 0 END AS spice_level_match
            FROM user_profile up
            LEFT JOIN rolled_out_item rolled_items ON 1=1
            LEFT JOIN meal_property mp ON rolled_items.item_id = mp.item_id
            WHERE up.user_id = {user_id} and date ={rolled_out_date}
            ORDER BY diet_match DESC,
                    spice_level_match DESC) preference;
            """
        next_day_menu = self.database.fetch_all(query)
        if(len(next_day_menu) == 0):
            query = """select item_id, item_name from rolled_out_item;"""
            next_day_menu = self.database.fetch_all(query)
    

# def main():
#     db = DatabaseServices('recommendation_engine.db')
#     item_services = ItemServices(db)
#     voted_items = [
#     (11, 1, 1, 12, 1, '2024-06-21 14:30:00'),
#     (21, 2, 2, 21, 1, '2024-06-21 14:30:00'),
#     (31, 3, 1, 30, 1, '2024-06-21 14:30:00'),
#     (41, 1, 2, 14, 1, '2024-06-21 14:30:00'),
#     (51, 2, 3, 32, 1, '2024-06-21 14:30:00'),
#     (61, 3, 1, 22, 1, '2024-06-21 14:30:00'),
#     (71, 1, 3, 33, 1, '2024-06-21 14:30:00'),
#     (81, 2, 2, 15, 1, '2024-06-21 14:30:00'),
#     (91, 3, 3, 38, 1, '2024-06-21 14:30:00'),
#     (101, 1, 1, 29, 1, '2024-06-21 14:30:00')
# ]

#     feedback = [
#     (10, 1, 12, 5, "Great item!", 0.8, '2024-06-21 14:30:00'),
#     (20, 2, 21, 4, "Good item.", 0.6, '2024-06-21 14:30:00'),
#     (30, 1, 30, 3, "Average item.", 0.4, '2024-06-21 14:30:00'),
#     (40, 3, 14, 5, "Amazing!", 0.9, '2024-06-21 14:30:00'),
#     (50, 2, 32, 2, "Could be better.", 0.2, '2024-06-21 14:30:00'),
#     (60, 1, 22, 4, "Delicious!", 0.7, '2024-06-21 14:30:00'),
#     (70, 3, 33, 3, "Not bad.", 0.5, '2024-06-21 14:30:00'),
#     (80, 2, 15, 5, "Excellent choice.", 0.85, '2024-06-21 14:30:00'),
#     (90, 1, 38, 2, "Tasty!", 0.75, '2024-06-21 14:30:00'),
#     (8, 3, 29, 4, "Satisfactory.", 0.6, '2024-06-21 14:30:00')
# ]

#     item_audit = [
#     (1, "Aloo Paratha", 6, '2024-06-21 14:30:00'),
#     (2, "Burger", 4, '2024-06-21 14:30:00'),
#     (3, "Bhindi", 3, '2024-06-21 14:30:00')
# ]

#     # notification = [
#     # ( 1, 3, "[(1, 'Aloo Paratha'), (2, 'Burger'),(3, 'Bhindi'),(4, 'Paneer')]"),
#     # ( 2, 4, "[(1, 'Aloo Paratha'), (2, 'Burger'),(3, 'Bhindi'),(4, 'Paneer')]"),
#     # ( 3, 7, "[(1, 'Aloo Paratha'), (2, 'Burger'),(3, 'Bhindi'),(4, 'Paneer')]"),
#     # ( 4, 5, "[(1, 'Aloo Paratha'), (2, 'Burger'),(3, 'Bhindi'),(4, 'Paneer')]")
#     # ]
# #     # Insert records
# #     # item_services.insert_into_meal_type([(1, 'breakfast'), (2, 'lunch'), (3, 'dinner')])
# #     # item_services.insert_into_items([(1, 'Aloo Paratha', 50.00, 1, True), (2, 'Burger', 40.00, 1, True), (3, 'Bhindi', 70.00, 2, True), (4, 'Paneer', 100.00, 2, True)])
#     item_services.insert_into_voted_items(voted_items)
#     item_services.insert_into_feedback(feedback)
#     item_services.insert_into_item_audit(item_audit)
# #     item_services.insert_into_notification(notification)
# if __name__ == '__main__':
#     main()
