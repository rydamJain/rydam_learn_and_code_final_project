import sqlite3
from threading import local

class DatabaseServices:
    def __init__(self, db_name):
        self.db_name = db_name
        self._local = local()
        self.create_tables()

    def _get_connection(self):
        if not hasattr(self._local, 'conn'):
            self._local.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        return self._local.conn

    def _get_cursor(self):
        if not hasattr(self._local, 'cursor'):
            self._local.cursor = self._get_connection().cursor()
        return self._local.cursor
    
    def drop_table(self):
        cursor = self._get_cursor()
        cursor.execute('''
        DROP TABLE notification
        ''')
        cursor.execute('''
        DROP TABLE feedback
        ''')
        self._get_connection().commit()

    def rename_table(self):
        cursor = self._get_cursor()
        cursor.execute('''
        ALTER TABLE items RENAME TO item;
        ''')
        cursor.execute('''
        ALTER TABLE roles RENAME TO role;
        ''')
        cursor.execute('''
        ALTER TABLE users RENAME TO user;
        ''')
        cursor.execute('''
        ALTER TABLE voted_items RENAME TO voted_item;
        ''')
        self._get_connection().commit()

    def create_tables(self):
        cursor = self._get_cursor()
        # Create roles table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS role (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        ''')
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            role_id INTEGER,
            FOREIGN KEY (role_id) REFERENCES role(id)
        )
        ''')
       
        # Create item table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS item (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price DECIMAL NOT NULL,
            meal_type_id INTEGER,
            availability_status BOOLEAN NOT NULL,
            FOREIGN KEY (meal_type_id) REFERENCES meal_type(id)
        )
        ''')

        # Create meal_type table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS meal_type (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
        )
        ''')

        # Create voted_item table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS voted_item (
        id INTEGER PRIMARY KEY,
        item_id INTEGER,
        meal_type_id INTEGER,
        user_id INTEGER,
        is_voted BOOLEAN NOT NULL,
        date TIMESTAMP NOT NULL,
        FOREIGN KEY (item_id) REFERENCES item(id),
        FOREIGN KEY (meal_type_id) REFERENCES meal_type(id),
        FOREIGN KEY (user_id) REFERENCES user(id)
        )
        ''')

        # Create feedback table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY,
        item_id INTEGER,
        user_id INTEGER,
        rating INTEGER NOT NULL,
        comment TEXT,
        sentiment_score DECIMAL,
        date TIMESTAMP NOT NULL,
        FOREIGN KEY (item_id) REFERENCES item(id),
        FOREIGN KEY (user_id) REFERENCES user(id)
        )
        ''')

     # Create item_audit table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS item_audit (
        id integer  PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        rating integer,
        sentiment_score decimal,
        feedback_date timestamp,
        FOREIGN KEY (item_id) REFERENCES item(id),
        FOREIGN KEY (feedback_date) REFERENCES feedback(date),
        FOREIGN KEY (rating) REFERENCES feedback(rating),
        FOREIGN KEY (sentiment_score) REFERENCES feedback(sentiment_score)
     )
      ''')

    # Create notification table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notification (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT NOT NULL,
        date string               
        )
        ''')
        
        self._get_connection().commit()

    def execute(self, query, params=()):
        cursor = self._get_cursor()
        cursor.execute(query, params)
        self._get_connection().commit()
        return cursor

    def executemany(self, query, params_list):
        cursor = self._get_cursor()
        cursor.executemany(query, params_list)
        self._get_connection().commit()
        return cursor

    def fetchall(self, query, params=()):
        cursor = self._get_cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def fetchone(self, query, params=()):
        cursor = self._get_cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    def close(self):
        if hasattr(self._local, 'cursor'):
            self._local.cursor.close()
        if hasattr(self._local, 'conn'):
            self._local.conn.close()


