import mysql.connector
from mysql.connector import Error
import csv
import os
import uuid


def connect_db():
    """Connect to MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Change to your MySQL user
            password='root'  # Change to your MySQL password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='root',  
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """Create the user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3) NOT NULL
            );
        """)
        print("Table user_data created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, file_path):
    """Insert data from CSV file into user_data table."""
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    try:
        cursor = connection.cursor()
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Generate UUID for user_id
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully.")
    except Error as e:
        print(f"Error inserting data: {e}")


if __name__ == "__main__":
    # Testing connection
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()

    connection = connect_to_prodev()
    if connection:
        create_table(connection)
        insert_data(connection, 'user_data.csv')
        connection.close()
