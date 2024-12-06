from seed import connect_to_prodev  # Assuming `seed.connect_to_prodev` is available

def paginate_users(page_size, offset):
    """
    Fetches a single page of data from the user_data table with a given page size and offset.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)  # Fetch rows as dictionaries
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    Lazily paginates data from the user_data table.

    Args:
        page_size (int): The number of rows per page.

    Yields:
        list: A list of rows representing a single page.
    """
    offset = 0
    while True:
        # Fetch the next page
        page = paginate_users(page_size, offset)
        if not page:
            # Stop iteration when no more data is available
            break
        yield page
        # Increment the offset by the page size for the next fetch
        offset += page_size
