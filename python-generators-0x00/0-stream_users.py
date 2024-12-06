import sqlite3

def stream_users():
    """Generator function to stream rows from the user_data table."""
    conn = sqlite3.connect('your_database.db')  
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user_data")
    
    for row in cursor:
        yield dict(row)  

    conn.close()
