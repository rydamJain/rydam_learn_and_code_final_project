import sys
sys.path.append("..")
from services.item_service import ItemServices

class AdminHandler:
    def __init__(self, database):
        self.item_services = ItemServices(database)

    def show_admin_options(self):
        options = """
        Admin options:
        1. Add item
        2. Delete item
        3. Update item
        4. See responses from employees
        Enter your choice:
        """
        return options

    def handle_choice(self, conn, choice):
        if choice == '1':
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

        elif choice == '2':
            conn.sendall("Enter item id:".encode())
            item_id = int(conn.recv(1024).decode().strip())
            self.item_services.delete_item(item_id)
            conn.sendall("Item deleted successfully.".encode())
        elif choice == '3':
            # Implement update item functionality
            pass
        elif choice == '4':
            print("See responses from employees")
        else:
            conn.sendall("Invalid choice. Please try again.".encode())
