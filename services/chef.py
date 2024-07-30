import sys
from datetime import datetime
sys.path.append("..")
from services.item_service import ItemServices
from recommendation_system.recommendation_algo import get_recommendation
import sqlite3

class ChefService:
    def __init__(self, database):
        self.item_services = ItemServices(database)
        self.database = database

    def show_chef_options(self):
        options = """
        Chef options:
        1. View menu 
        2. Roll out menu
        3. See responses 
        4. View Recommendations
        5. Discard Menu items
        6. Get Detailed feedback from employees
        7. Exit
        Enter your choice:
        """
        return options

    def handle_choice(self, conn, choice):
        if choice == '1':
            self.view_menu(conn)
        elif choice == '2':
            self.roll_out_menu(conn)
        elif choice == '3':
            conn.sendall("Please enter date for which you want to see voted_items\n:".encode())
            date = conn.recv(1024).decode()
            self.get_response(conn,date)
        elif choice == '4':
            recommended_items = self.view_recommendations(conn)
            conn.sendall(f"Recommendations are : {recommended_items}".encode())

        elif choice == '5':
            self.discard_menu_item(conn)
        elif choice == '6':
            self.get_detailed_feedback(conn)
        elif choice == '7':
            return
        else:
            conn.sendall("Invalid choice. Please try again.".encode())

    def view_menu(self, conn):
        items = self.database.fetchall("SELECT * FROM item")
        for item in items:
            conn.sendall(f"Item ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Meal Type ID: {item[3]}, Availability: {'Available' if item[4] else 'Not Available'}\n".encode())

    def get_response(self, conn,date):
        query = "SELECT * FROM voted_item WHERE date = ?"
        voted_items = self.database.fetchall(query, (date,))
        for item in voted_items:
            conn.sendall(f"ID: {item[0]}, Item ID: {item[1]}, Meal Type ID: {item[2]}, UserID: {item[3]}\n".encode())

    def roll_out_menu(self,conn):
        try:
            conn.sendall("Please enter items to roll out (format: item_id,item_name,meal_type_id;item_id,item_name,meal_type_id;...):\n".encode())
            rolled_out_items = conn.recv(1024).decode()
            roll_out_date = str(datetime.today().date())
            # Split the input into individual items
            items = rolled_out_items.split(';')
            query = "INSERT INTO rolled_out_item (item_id, item_name, meal_type_id, date) VALUES (?, ?, ?, ?)"
            for item in items:
                if item.strip():  
                    item_id, item_name, meal_type_id = item.split(',')
                    self.database.execute(query, (item_id.strip(), item_name.strip(), meal_type_id.strip(), roll_out_date))
            message = "New Items rolled out."
            self.send_notification(conn,message)
            
        
        except Exception as e:
            # Handle any errors that occur
            conn.sendall(f"An error occurred: {str(e)}\n".encode())
            self.database.rollback() 
        
    def send_notification(self, conn,message): 
        notification_date = str(datetime.today().date())
        self.database.execute("INSERT INTO notification (message, date) VALUES (?, ?)", (message, notification_date))
        conn.sendall(f"Notification ({message}) sent successfully!\n".encode())

    def view_recommendations(self,conn):
        conn.sendall("Please enter meal_type_id for which you want to see recommendations\n:".encode())
        meal_type_id = conn.recv(1024).decode()
        conn.sendall("Please enter date for which you want to see recommendations\n:".encode())
        target_date = conn.recv(1024).decode()
        recommended_items = get_recommendation(meal_type_id,target_date)
        return recommended_items
    
    def get_detailed_feedback(self,conn):
        try:
            message = f"Some items are added in discarded menu please provide your detailed feedback for those items."
            self.send_notification(conn,message)
            
        except Exception as e:
            conn.sendall(f"An error occurred: {str(e)}\n".encode())

    def discarded_item_view(self):
        drop_query = "DROP VIEW IF EXISTS discarded_item"
        create_query = """
        CREATE VIEW discarded_item AS
        SELECT item_id, AVG(rating) AS average_rating, AVG(sentiment_score) AS average_sentiment
        FROM feedback
        GROUP BY item_id
        HAVING AVG(rating) < 2 AND AVG(sentiment_score) < 0.5
         """
        try:
            self.database.execute(drop_query)
            self.database.execute(create_query)
            print("View discarded_item created successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    
    def discard_menu_item(self,conn):    
            self.discarded_item_view()
            conn.sendall("Please enter item_id to delete\n:".encode())
            item_id = conn.recv(1024).decode()
            query = f"""delete from item where id={item_id};"""
            self.database.execute(query)
            print("Item deleted successfully!")
