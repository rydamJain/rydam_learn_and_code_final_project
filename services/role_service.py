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


db = DatabaseServices('recommendation_engine.db')
role_services = RoleServices(db)
# role_services.insert_role(3, "employee")
# role_services.insert_role(2, "chef")
# role_services.insert_role(1, "admin")
# role_services.delete_role(2)
print(role_services.fetch_roles())
print(role_services.get_role_id_by_email("hemish@gmail.com"))