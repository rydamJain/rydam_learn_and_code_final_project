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
        4. View rolled out items 
        5. Choose item
        6. Provide feedback for discarded items
        Enter your choice:
        """
        return options

    def handle_choice(self, connection, choice):
        if choice == '1':
            self.view_menu(connection)
        elif choice == '2':
            notification_date = str(datetime.today().date())
            self.watch_notifications(connection,notification_date)
        elif choice == '3':
            self.provide_feedback(connection)
        elif choice == '4':
            self.view_rolled_out_items(connection)   
        elif choice == '5':
            self.vote_item(connection)
        elif choice == '6':
            self.detailed_feedback_of_discarded_item(connection)
        else:
            connection.sendall("Invalid choice. Please try again.".encode())

    def view_menu(self, connection):
        items = self.database.fetchall("SELECT * FROM item")
        for item in items:
            connection.sendall(f"Item ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Meal Type ID: {item[3]}, Availability: {'Available' if item[4] else 'Not Available'}\n".encode())

    def watch_notifications(self, connection, notification_date):
        notifications = self.database.fetchall("SELECT * FROM notification WHERE date = ?", (notification_date,))
        for notification in notifications:
            connection.sendall(f"Notification ID: {notification[0]}, Message: {notification[1]}, Notification Date: {notification[2]}\n".encode())

    def provide_feedback(self, connection):
        connection.sendall("Enter item id:".encode())
        item_id = int(connection.recv(1024).decode().strip())

        connection.sendall("Enter user id:".encode())
        user_id = int(connection.recv(1024).decode().strip())

        connection.sendall("Enter your feedback comment:".encode())
        comment = connection.recv(1024).decode().strip()

        sentiment_score = get_sentiment_score(comment)

        connection.sendall("Enter your rating (1-5):".encode())
        rating = int(connection.recv(1024).decode().strip())
        connection.sendall("Enter the date (YYYY-MM-DD):".encode())
        date = connection.recv(1024).decode().strip()

        query = '''
        INSERT INTO feedback (item_id, user_id, rating, comment,sentiment_score, date)
        VALUES (?, ?, ?, ?, ?,?)
        '''
        self.database.execute(query, (item_id, user_id, rating, comment, sentiment_score,date))
        connection.sendall("Feedback submitted successfully.".encode())

    def view_rolled_out_items(self,connection):
        rolled_out_date = str(datetime.today().date()) 
        items = self.database.fetchall("SELECT * FROM rolled_out_item WHERE date=?", (rolled_out_date,))
        for item in items:
            connection.sendall(f"Item ID: {item[0]},Item Name: {item[1]}, Meal Type ID: {item[2]}\n".encode())

    def vote_item(self,connection):
        try:
            connection.sendall("Enter voted item id:".encode())
            voted_item_id = int(connection.recv(1024).decode().strip())

            connection.sendall("Enter item id:".encode())
            item_id = int(connection.recv(1024).decode().strip())

            connection.sendall("Enter meal type id:".encode())
            meal_type_id = int(connection.recv(1024).decode().strip())

            connection.sendall("Enter user id:".encode())
            user_id = int(connection.recv(1024).decode().strip())

            connection.sendall("Enter voting status (1 for voted, 0 for not voted):".encode())
            is_voted = bool(int(connection.recv(1024).decode().strip()))

            connection.sendall("Enter the date (YYYY-MM-DD):".encode())
            date = connection.recv(1024).decode().strip()
            date = datetime.strptime(date, "%Y-%m-%d")

            query = '''
            INSERT INTO voted_items (id, item_id, meal_type_id, user_id, is_voted, date)
            VALUES (?, ?, ?, ?, ?, ?)
            '''
            params = (voted_item_id, item_id, meal_type_id, user_id, is_voted, date)
            self.database.execute(query, params)

            connection.sendall("Item voted successfully.".encode())
    
        except Exception as e:
            connection.sendall(f"An error occurred: {e}".encode())

    def detailed_feedback_of_discarded_item(self,connection):
        connection.sendall("Enter item id:".encode())
        item_id = int(connection.recv(1024).decode().strip())

        connection.sendall("Enter user id:".encode())
        user_id = int(connection.recv(1024).decode().strip())

        connection.sendall("What taste you want to have:".encode())
        like = connection.recv(1024).decode().strip()

        connection.sendall("What you disliked about the item:".encode())
        dislike = int(connection.recv(1024).decode().strip())
       
        connection.sendall("Would you provide home recipe for the item:".encode())
        home_recipe = int(connection.recv(1024).decode().strip())

        query = '''
        INSERT INTO discarded_item_detailed_feedback (item_id, user_id, like, dislike,home_recipe)
        VALUES (?, ?, ?, ?, ?)
        '''
        self.database.execute(query, (item_id, user_id, like, dislike, home_recipe))
        connection.sendall("Detailed Feedback submitted successfully.".encode())


        
