import sqlite3
import functools

def log_queries():
    """
    A decorator to log SQL queries before executing them.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Log the query from the arguments
            query = kwargs.get('query', args[0] if args else None)
            if query:
                print(f"Executing SQL query: {query}")
            else:
                print("No SQL query provided.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    """
    Fetch all users from the database based on the provided query.

    Args:
        query (str): SQL query to execute.

    Returns:
        list: List of rows fetched from the database.
    """
    conn = sqlite3.connect('users.db')  
    cursor = conn.cursor()
    cursor.execute(query)  
    results = cursor.fetchall()  
    conn.close()  
    return results

# Fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    for user in users:
        print(user)
