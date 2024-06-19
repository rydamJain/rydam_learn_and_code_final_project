import sys
sys.path.append("..")
from recommendation_system.setup_database import DatabaseServices

class UserServices:
    def __init__(self, database):
        self.db = database

    def insert_user(self, id, email, role_id):
        self.db.execute('''
        INSERT INTO users (id, email, role_id) VALUES (?, ?, ?)
        ''', (id, email, role_id))

    def delete_user(self, id):
        self.db.execute('''
        DELETE FROM users WHERE id = ?
        ''', (id,))

    def fetch_users(self):
        return self.db.fetchall('SELECT * FROM users')

    

db = DatabaseServices('recommendation_engine.db')
user_services = UserServices(db)
# user_services.insert_user(1, "rydam@gmail.com", 1)
# user_services.insert_user(2, "hemish@gmail.com", 2)
# user_services.insert_user(3, "nidhi@gmail.com", 3)
# user_services.insert_user(4, "naman@gmail.com", 3)
# user_services.insert_user(5, "kashish@gmail.com", 3)
# user_services.insert_user(6, "ahana@gmail.com", 3)
# user_services.delete_user(1)
# print(user_services.fetch_users())

