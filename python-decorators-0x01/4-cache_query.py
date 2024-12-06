import time
import sqlite3
import functools

# Cache dictionary to store query results
query_cache = {}

def with_db_connection(func):
    """
    A decorator that opens a database connection, passes it to the function,
    and ensures the connection is closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Connect to the SQLite database
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()  # Close the connection after the function execution
        return result
    return wrapper

def cache_query(func):
    """
    A decorator that caches the results of database queries to avoid redundant calls.
    It stores results in a global `query_cache` dictionary, indexed by query string.
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Check if the query result is already cached
        if query in query_cache:
            print("Returning cached result for query:", query)
            return query_cache[query]  # Return cached result
        else:
            # If the result is not cached, execute the query
            result = func(conn, query, *args, **kwargs)
            query_cache[query] = result  # Cache the result for future calls
            print("Query result cached for query:", query)
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users from the database. If the query has been executed before,
    it returns the cached result.

    Args:
        conn (sqlite3.Connection): The database connection.
        query (str): The SQL query to execute.

    Returns:
        list: The query result as a list of tuples.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Example1
if __name__ == "__main__":
    # First call will execute the query and cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)
    #  second 
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
