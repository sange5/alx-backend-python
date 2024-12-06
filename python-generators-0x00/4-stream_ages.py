import sqlite3

def stream_user_ages():
    """
    Generator to stream user ages one by one from the user_data table.

    Yields:
        int: Age of each user.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('your_database.db')  # Replace with your database file
    cursor = conn.cursor()
    
    # Execute the query to fetch only the age column from user_data table
    cursor.execute("SELECT age FROM user_data")
    
    # Yield each age one by one
    for row in cursor:
        yield row[0]  # Access the age field directly (assuming it's the first column)

    # Close the connection
    conn.close()

def calculate_average_age():
    """
    Calculate the average age using the stream_user_ages generator.

    Prints:
        The average age of users.
    """
    total_age = 0
    count = 0

    # Use the generator to iterate over ages
    for age in stream_user_ages():
        total_age += age
        count += 1

    # Calculate and print the average
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users in the dataset.")
