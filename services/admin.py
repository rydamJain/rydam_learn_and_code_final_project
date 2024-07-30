import sys
sys.path.append("..")
from services.item_service import ItemServices

class AdminHandler:
    def __init__(self, database):
        self.database = database
        self.item_services = ItemServices(database)
       

    def show_admin_options(self):
        options = """
        Admin options:
        1. Add item
        2. Delete item
        3. Update item
        4. View feedbacks 
        Enter your choice:
        """
        return options

    def handle_choice(self, conn, choice):
        if choice == '1':
            self.add_item(conn)
        elif choice == '2':
            self.delete_item(conn)
        elif choice == '3':
            self.update_item(conn)
        elif choice == '4':
            self.view_feedbacks(conn)
        else:
            conn.sendall("Invalid choice. Please try again.".encode())

    def add_item(self, conn):
        conn.sendall("Enter item id:".encode())
        item_id = int(conn.recv(1024).decode().strip())

        conn.sendall("Enter item name:".encode())
        name = conn.recv(1024).decode().strip()

        conn.sendall("Enter item price:".encode())
        price = float(conn.recv(1024).decode().strip())

        conn.sendall("Enter meal type id:".encode())
        meal_type_id = int(conn.recv(1024).decode().strip())

        conn.sendall("Enter availability status (1 for available, 0 for not available):".encode())
        availability_status = bool(int(conn.recv(1024).decode().strip()))

        # Call the appropriate method from ItemServices to add the item
        self.item_services.insert_into_items([(item_id, name, price, meal_type_id, availability_status)])
        conn.sendall("Item added successfully.".encode())

    def delete_item(self, conn):
        conn.sendall("Enter item id:".encode())
        item_id = int(conn.recv(1024).decode().strip())
        self.item_services.delete_item(item_id)
        conn.sendall("Item deleted successfully.".encode())

    def update_item(self, conn):
        conn.sendall("Enter item id to update availability status:".encode())
        item_id = int(conn.recv(1024).decode().strip())

        conn.sendall("Enter new availability status (1 for available, 0 for not available):".encode())
        availability_status = bool(int(conn.recv(1024).decode().strip()))

        self.item_services.update_availability_status(item_id, availability_status)
        conn.sendall("Item availability status updated successfully.".encode())

    def view_feedbacks(self, connection):
        feedbacks = self.database.fetchall("SELECT * FROM feedback")
        for feedback in feedbacks:
            connection.sendall(f"Item ID: {feedback[1]}, User ID: {feedback[2]}, Rating: {feedback[3]}, Comment: {feedback[4]},  Sentiment Score: {feedback[5]}\n".encode())
