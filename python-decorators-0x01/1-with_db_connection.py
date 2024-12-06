import sqlite3
import functools

def with_db_connection(func):
    """
    A decorator that opens a database connection, passes it to the function,
    and ensures the connection is closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Establish database connection
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection object to the wrapped function
            result = func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is closed
            conn.close()
        return result
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetch a user by their ID from the database.

    Args:
        conn (sqlite3.Connection): The database connection.
        user_id (int): The ID of the user to fetch.

    Returns:
        tuple: The user's record from the database.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
