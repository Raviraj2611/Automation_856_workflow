import sqlite3
from ErrorHandler.error_handler import db_error

def create_db_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        print("Database connection established.")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        db_error("Error connecting to database","Error")
        return None
