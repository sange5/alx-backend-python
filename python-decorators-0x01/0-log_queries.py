import sqlite3
import functools
from datetime import datetime  # Import datetime for logging timestamps

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Capture the current timestamp
        query_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Log the query with its timestamp
        print(f"[{query_time}] Executing query: {args[1]}")  # Assuming the SQL query is the second argument
        
        # Call the original function to execute the query
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
