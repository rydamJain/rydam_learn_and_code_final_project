import sys
sys.path.append("..")
from recommendation_system.setup_database import DatabaseServices

class RoleServices:
    def __init__(self, database):
        self.db = database

    def insert_role(self, role_id, name):
        self.db.execute('''
        INSERT OR IGNORE INTO roles (id, name) VALUES (?, ?)
        ''', (role_id, name))

    def delete_role(self, role_id):
        self.db.execute('''
        DELETE FROM roles WHERE id = ?
        ''', (role_id,))

    def fetch_roles(self):
        return self.db.fetchall('SELECT * FROM roles')

    def get_role_id_by_email(self, email):
        result = self.db.fetchall('''
        SELECT role_id FROM users WHERE email = ?
        ''', (email,))
        if result:
            return result[0][0]
        return None

    def get_role_name_by_id(self, role_id):
        result = self.db.fetchall('''
        SELECT name FROM roles WHERE id = ?
        ''', (role_id,))
        if result:
            return result[0][0]
        return None

    def show_role_based_options(self,role_name):
        if role_name == "admin":
            print("Logged in as Admin")
            return "1. Add item\n2. Delete item\n3. Update item\nEnter your choice:"
        elif role_name == "employee":
            print("Logged in as Employee")
            return "1. View menu\n2. Choose item\n3. Provide feedback\nEnter your choice:"
        elif role_name == "chef":
            print("Logged in as Chef")
            return "1. Roll out menu\n2. See response\nEnter your choice:"
        else:
            return "Unknown role. Connection closin g."

db = DatabaseServices('recommendation_engine.db')
role_services = RoleServices(db)
# role_services.insert_role(3, "employee")
# role_services.insert_role(2, "chef")
# role_services.insert_role(1, "admin")
# role_services.delete_role(2)
# print(role_services.fetch_roles())
# print(role_services.get_role_id_by_email("hemish@gmail.com"))