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

def transactional(func):
    """
    A decorator that wraps a database operation in a transaction.
    Commits the transaction if the function succeeds, otherwise rolls back.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Call the wrapped function
            result = func(conn, *args, **kwargs)
            # Commit the transaction if no error occurs
            conn.commit()
            return result
        except Exception as e:
            # Roll back the transaction on any error
            conn.rollback()
            raise e  # Re-raise the exception for further handling
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update the email of a user in the database.

    Args:
        conn (sqlite3.Connection): The database connection.
        user_id (int): The ID of the user to update.
        new_email (str): The new email address to set.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
if __name__ == "__main__":
    try:
        update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
        print("Email updated successfully.")
    except Exception as e:
        print(f"Failed to update email: {e}")
