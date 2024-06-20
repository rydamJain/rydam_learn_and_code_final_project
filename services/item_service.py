import sys
sys.path.append("..")
from recommendation_system.setup_database import DatabaseServices

class ItemServices:
    def __init__(self, database):
        self.db = database

    def insert_into_meal_type(self, meal_types):
        self.db.executemany('''
        INSERT INTO meal_type (id, name) VALUES (?, ?)
        ''', meal_types)

    def insert_into_items(self, items):
        
        self.db.executemany('''
        INSERT INTO items (id, name, price, meal_type_id, availability_status) VALUES (?, ?, ?, ?, ?)
        ''', items)
        print("Item added successfully.")

    def delete_item(self, item_id):
        query = 'DELETE FROM items WHERE id = ?'
        params = (item_id,)
        self.db.execute(query, params)
        print("Item deleted successfully.")

    def update_availability_status(self, item_id, availability_status):
        query = 'UPDATE items SET availability_status = ? WHERE id = ?'
        params = (availability_status, item_id)
        self.db.execute(query, params)
        print("Item availability status updated successfully.")

    def insert_into_voted_items(self, voted_items):
        self.db.executemany('''
        INSERT INTO voted_items (id, item_id, meal_type_id, user_id, is_voted, date) VALUES (?, ?, ?, ?, ?, ?)
        ''', voted_items)

    def insert_into_feedback(self, feedback):
        self.db.executemany('''
        INSERT INTO feedback (id, item_id, user_id, rating, comment,sentiment_score, date) VALUES (?, ?, ?, ?, ?,?, ?)
        ''', feedback)

    def insert_into_item_audit(self, item_audits):
        self.db.executemany('''
        INSERT INTO item_audit (item_id, name, cooked_number_of_times, audit_date) VALUES (?, ?, ?, ?)
        ''', item_audits)

    def insert_into_notification(self, notifications):
        self.db.executemany('''
        INSERT INTO notification (id, user_id, message) VALUES ( ?, ?, ?)
        ''', notifications)

    

# def main():
#     db = DatabaseServices('recommendation_engine.db')
#     item_services = ItemServices(db)
# #     voted_items = [
# #     (1, 1, 1, 101, True, '2023-03-01 10:00:00'),
# #     (2, 2, 2, 241, True, '2023-03-01 11:00:00'),
# #     (3, 3, 3, 343, True, '2023-03-01 12:00:00'),
# #     (4, 4, 3, 78, True, '2023-03-01 12:00:00')
# #     ]

#     feedback = [
#     (1, 1, 101, 5, 'Great!',0.80, '2023-03-01 10:00:00'),
#     (2, 2, 241, 4, 'Good', 0.70, '2023-03-01 11:00:00'),
#     (3, 3, 343, 3, 'Okay', 0.50, '2023-03-01 12:00:00'),
#     (4, 4, 78, 5, 'Awesome', 1.00, '2023-03-01 12:00:00')
#     ]

#     item_audit = [
#     (1, 'Aloo Paratha', 15, '2023-03-01 10:00:00'),
#     (2, 'Burger', 25, '2023-03-01 11:00:00'),
#     (3, 'Bhindi', 40, '2023-03-01 12:00:00'),
#     (4, 'Paneer', 50, '2023-03-01 12:00:00')
#     ]

    # notification = [
    # ( 1, 3, "[(1, 'Aloo Paratha'), (2, 'Burger'),(3, 'Bhindi'),(4, 'Paneer')]"),
    # ( 2, 4, "[(1, 'Aloo Paratha'), (2, 'Burger'),(3, 'Bhindi'),(4, 'Paneer')]"),
    # ( 3, 7, "[(1, 'Aloo Paratha'), (2, 'Burger'),(3, 'Bhindi'),(4, 'Paneer')]"),
    # ( 4, 5, "[(1, 'Aloo Paratha'), (2, 'Burger'),(3, 'Bhindi'),(4, 'Paneer')]")
    # ]
#     # Insert records
#     # item_services.insert_into_meal_type([(1, 'breakfast'), (2, 'lunch'), (3, 'dinner')])
#     # item_services.insert_into_items([(1, 'Aloo Paratha', 50.00, 1, True), (2, 'Burger', 40.00, 1, True), (3, 'Bhindi', 70.00, 2, True), (4, 'Paneer', 100.00, 2, True)])
#     # item_services.insert_into_voted_items(voted_items)
    # item_services.insert_into_feedback(feedback)
#     # item_services.insert_into_item_audit(item_audit)
#     item_services.insert_into_notification(notification)
# if __name__ == '__main__':
#     main()
