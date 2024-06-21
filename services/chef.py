import sys
from datetime import datetime
sys.path.append("..")
from services.item_service import ItemServices
from recommendation_system.sentiment_analysis import get_sentiment_score

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
        4. Exit
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
            return
        else:
            conn.sendall("Invalid choice. Please try again.".encode())

    def view_menu(self, conn):
        items = self.database.fetchall("SELECT * FROM items")
        for item in items:
            conn.sendall(f"Item ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Meal Type ID: {item[3]}, Availability: {'Available' if item[4] else 'Not Available'}\n".encode())

    def get_response(self, conn,date):
        query = "SELECT * FROM voted_items WHERE date = ?"
        voted_items = self.database.fetchall(query, (date,))
        for item in voted_items:
            conn.sendall(f"ID: {item[0]}, ITem ID: {item[1]}, Meal Type ID: {item[2]}, UserID: {item[3]}\n".encode())

  