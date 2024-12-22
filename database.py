import sqlite3

def connect_db(db_name='sales.db'):
    return sqlite3.connect(db_name)