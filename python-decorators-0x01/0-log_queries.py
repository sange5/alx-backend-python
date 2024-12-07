import sqlite3
import functools
from datetime import datetime  

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"[{query_time}] Executing query: {args[1]}")  
        
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

users = fetch_all_users(query="SELECT * FROM users")
