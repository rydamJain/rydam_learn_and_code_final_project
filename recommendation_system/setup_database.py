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

    def create_tables(self):
        cursor = self._get_cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            role_id INTEGER,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
        ''')
        # cursor.execute('''
        # CREATE TABLE IF NOT EXISTS meal_type (
        #     id INTEGER PRIMARY KEY,
        #     name TEXT NOT NULL,
        #     FOREIGN KEY (id) REFERENCES voted_items(category_id),
        #     FOREIGN KEY (id) REFERENCES items(category_id),
        # )
        # ''')
        
        self._get_connection().commit()

    def execute(self, query, params=()):
        cursor = self._get_cursor()
        cursor.execute(query, params)
        self._get_connection().commit()
        return cursor

    def fetchall(self, query, params=()):
        cursor = self._get_cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        if hasattr(self._local, 'cursor'):
            self._local.cursor.close()
        if hasattr(self._local, 'conn'):
            self._local.conn.close()
