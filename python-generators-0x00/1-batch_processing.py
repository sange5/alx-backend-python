import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator function to fetch users in batches from the database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # Replace with your MySQL username
            password="your_password",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM user_data;")
        total_users = cursor.fetchone()["COUNT(*)"]
        offset = 0

        while offset < total_users:
            cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset};")
            rows = cursor.fetchall()
            if not rows:
                break
            yield rows  # Use yield to return the batch as a generator
            offset += batch_size

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        processed_users = [user for user in batch if user["age"] > 25]
        for user in processed_users:
            print(user)
