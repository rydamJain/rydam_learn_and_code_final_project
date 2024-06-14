from setup_database import DatabaseServices

class RoleServices:
    def __init__(self, database):
        self.db = database

    def insert_role(self, role_id, name):
        self.db.execute('''
        INSERT OR IGNORE INTO roles (id, name) VALUES (?, ?)
        ''', (role_id, name))

    def delete_role(self, role_id):
        self.db.execute(f'''
        DELETE FROM  roles  WHERE id = {role_id}
        ''')

    def fetch_roles(self):
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM roles')
        roles = cursor.fetchall()
        return roles

    def get_role_id_by_email(self, email):
        cursor = self.db.conn.cursor()
        cursor.execute('''
        SELECT role_id FROM users WHERE email = ?
        ''', (email,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None

db = DatabaseServices('recommendation_engine.db')
role_services = RoleServices(db)
# role_services.insert_role( 2, "chef")
# role_services.insert_role( 3, "employee")
# role_services.delete_role(2)
print(role_services.fetch_roles())