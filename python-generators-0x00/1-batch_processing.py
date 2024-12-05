import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Fetch users from the database in batches.
    :param batch_size: Number of rows per batch.
    :yield: List of rows (as dictionaries).
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM user_data")
    total_rows = cursor.fetchone()['total']
    
    for offset in range(0, total_rows, batch_size):
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        if rows:
            yield rows

    cursor.close()
    connection.close()
