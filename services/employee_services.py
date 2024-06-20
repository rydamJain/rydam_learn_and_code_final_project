import sys
from datetime import datetime
sys.path.append("..")
from services.item_service import ItemServices
from recommendation_system.sentiment_analysis import get_sentiment_score

class EmployeeService:
    def __init__(self, database):
        self.item_services = ItemServices(database)
        self.database = database

    def show_employee_options(self):
        options = """
        Employee options:
        1. View menu 
        2. Watch notification 
        3. Provide feedback / comment
        4. Choose item 
        Enter your choice:
        """
        return options

    def handle_choice(self, conn, choice,user_id):
        if choice == '1':
            self.view_menu(conn)
        elif choice == '2':
            self.watch_notifications(conn,user_id)
        elif choice == '3':
            self.provide_feedback(conn)
        elif choice == '4':
            self.vote_item(conn)
        else:
            conn.sendall("Invalid choice. Please try again.".encode())

    def view_menu(self, conn):
        items = self.database.fetchall("SELECT * FROM items")
        for item in items:
            conn.sendall(f"Item ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Meal Type ID: {item[3]}, Availability: {'Available' if item[4] else 'Not Available'}\n".encode())

    def watch_notifications(self, conn,user_id):
        notifications = self.database.fetchall(f"SELECT * FROM notification where user_id = {user_id} ")
        for notification in notifications:
            conn.sendall(f"Notification ID: {notification[0]}, User ID: {notification[1]}, Message: {notification[2]}\n".encode())

    def provide_feedback(self, conn):
        conn.sendall("Enter item id:".encode())
        item_id = int(conn.recv(1024).decode().strip())

        conn.sendall("Enter user id:".encode())
        user_id = int(conn.recv(1024).decode().strip())

        conn.sendall("Enter your feedback comment:".encode())
        comment = conn.recv(1024).decode().strip()

        sentiment_score = get_sentiment_score(comment)

        conn.sendall("Enter your rating (1-5):".encode())
        rating = int(conn.recv(1024).decode().strip())
        conn.sendall("Enter the date (YYYY-MM-DD):".encode())
        date = conn.recv(1024).decode().strip()

        query = '''
        INSERT INTO feedback (item_id, user_id, rating, comment,sentiment_score, date)
        VALUES (?, ?, ?, ?, ?,?)
        '''
        self.database.execute(query, (item_id, user_id, rating, comment, sentiment_score,date))
        conn.sendall("Feedback submitted successfully.".encode())

    
    def vote_item(self,conn):
        try:
            conn.sendall("Enter voted item id:".encode())
            voted_item_id = int(conn.recv(1024).decode().strip())

            conn.sendall("Enter item id:".encode())
            item_id = int(conn.recv(1024).decode().strip())

            conn.sendall("Enter meal type id:".encode())
            meal_type_id = int(conn.recv(1024).decode().strip())

            conn.sendall("Enter user id:".encode())
            user_id = int(conn.recv(1024).decode().strip())

            conn.sendall("Enter voting status (1 for voted, 0 for not voted):".encode())
            is_voted = bool(int(conn.recv(1024).decode().strip()))

            conn.sendall("Enter the date (YYYY-MM-DD):".encode())
            date = conn.recv(1024).decode().strip()
            date = datetime.strptime(date, "%Y-%m-%d")

            query = '''
            INSERT INTO voted_items (id, item_id, meal_type_id, user_id, is_voted, date)
            VALUES (?, ?, ?, ?, ?, ?)
            '''
            params = (voted_item_id, item_id, meal_type_id, user_id, is_voted, date)
            self.database.execute(query, params)

            conn.sendall("Item voted successfully.".encode())
    
        except Exception as e:
            conn.sendall(f"An error occurred: {e}".encode())




        
