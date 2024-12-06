import time
import sqlite3
import functools

def with_db_connection(func):
    """
    A decorator that opens a database connection, passes it to the function,
    and ensures the connection is closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    A decorator that retries a function on failure due to transient errors.

    Args:
        retries (int): Number of retries before giving up.
        delay (int): Delay (in seconds) between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:  # Handle transient errors
                    print(f"Attempt {attempt} failed: {e}")
                    last_exception = e
                    time.sleep(delay)
            # Raise the last exception if all retries fail
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users from the database.

    Args:
        conn (sqlite3.Connection): The database connection.

    Returns:
        list: A list of user records.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print(users)
    except Exception as e:
        print(f"Failed to fetch users: {e}")
