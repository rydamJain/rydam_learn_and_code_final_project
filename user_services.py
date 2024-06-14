from setup_database import DatabaseServices

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

# Initialize the database and user services
db = DatabaseServices('recommendation_engine.db')
user_services = UserServices(db)

# Uncomment the following lines to insert users into the database
# user_services.insert_user(1, "rydam@gmail.com", 1)
# user_services.insert_user(2, "hemish@gmail.com", 2)
# user_services.insert_user(3, "nidhi@gmail.com", 3)
# user_services.insert_user(4, "ahaana@gmail.com", 3)
# user_services.insert_user(6, "john@gmail.com", 3)
# user_services.insert_user(5, "naman@gmail.com", 3)
# user_services.delete_user(5)
# Fetch and print all users
users = user_services.fetch_users()
print(users)