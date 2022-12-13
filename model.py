import sqlite3
from datetime import datetime

class Models:

    def __init__(self):
        self.db =  sqlite3.connect('database.db',check_same_thread=False)
        self.cursor = self.db.cursor()
        self.create_table()

    def create_table(self):
        """Creates table if not exists"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            chat_id TEXT PRIMARY KEY NOT NULL, 
            first_name TEXT DEFAULT "",
            last_name TEXT DEFAULT "",
            subsdate DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.db.commit()

    def add_user(self, chat_id, first_name, last_name):
        """Adds people to database"""
        self.cursor.execute('''
        INSERT INTO subscriptions (chat_id, first_name, last_name) VALUES (?, ?, ?)
        ''', (chat_id, first_name, last_name))
        self.db.commit()

    def delete_person(self, chat_id):
        """Deletes people from database"""
        self.cursor.execute('''
        DELETE FROM subscriptions WHERE chat_id = ?
        ''', (chat_id,))
        self.db.commit()
        
    def check_person(self, chat_id):
        """Checks if people exists"""
        self.cursor.execute('''
        SELECT * FROM subscriptions WHERE chat_id = ?
        ''', (chat_id,))
        return self.cursor.fetchone()

    def check_all(self):
        self.cursor.execute('''
        SELECT * FROM subscriptions 
        ''')
        return self.cursor.fetchall()
        
