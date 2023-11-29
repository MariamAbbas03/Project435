"""
Module that contains functions for connecting to and managing an SQLite3 database for an ecommerce inventory.
"""

import sqlite3

def connect_to_db():
    """
    Establishes a connection to the SQLite3 database 'ecommerce_inventory.db'.
    
    :return: The established connection object.
    :rtype: sqlite3.Connection
    """
    conn = sqlite3.connect('ecommerce_inventory.db')
    return conn

def create_inventory_table():
    """
    Creates a table named 'inventory' in the SQLite3 database if it does not already exist.

    The table contains columns for item_id, name, category, price_per_item, description, and count_in_stock.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT CHECK(category IN ('food', 'clothes', 'accessories', 'electronics')) NOT NULL,
                price_per_item REAL NOT NULL,
                description TEXT,
                count_in_stock INTEGER NOT NULL
            );
        ''')
        conn.commit()
        print("Inventory table created successfully")
    except Exception as e:
        print(f"Error creating inventory table: {e}")
    finally:
        conn.close()

def add_item(item):
    """
    Inserts a new item record into the 'inventory' table.

    :param item: A dictionary containing the item's details, including name, category, 
                 price_per_item, description, and count_in_stock.
    :type item: dict

    :return: A dictionary containing the inserted item's details or an error message.
    :rtype: dict

    :raises: Exception if an error occurs during the database operation.
    """
    added_item = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO inventory (name, category, price_per_item, description, count_in_stock)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            item['name'],
            item['category'],
            item['price_per_item'],
            item['description'],
            item['count_in_stock']
        ))
        conn.commit()
        added_item = get_item_by_id(cur.lastrowid)
    except Exception as e:
        conn.rollback()
        added_item = {"error": f"Error adding item: {e}"}
    finally:
        conn.close()
    return added_item

def get_all_items():
    """
    Retrieves all items from the 'inventory' table.

    :return: A list of dictionaries, where each dictionary represents an item.
    :rtype: list

    :raises: Exception if an error occurs during the database operation.
    """
    items = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory")
        rows = cur.fetchall()

        for row in rows:
            item = dict(row)
            items.append(item)

    except Exception as e:
        print(f"Error getting all items: {e}")
    finally:
        conn.close()

    return items

def get_item_by_id(item_id):
    """
    Retrieves an item from the 'inventory' table by its item_id.

    :param item_id: The unique identifier for the item.
    :type item_id: int

    :return: A dictionary containing the item's details.
    :rtype: dict

    :raises: Exception if an error occurs during the database operation.
    """
    item = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory WHERE item_id = ?", (item_id,))
        row = cur.fetchone()

        if row:
            item = dict(row)

    except Exception as e:
        print(f"Error getting item by ID: {e}")
    finally:
        conn.close()

    return item

def get_item_by_name(item_name):
    """
    Retrieves an item from the 'inventory' table by its name.

    :param item_name: The name of the item.
    :type item_name: str

    :return: A dictionary containing the item's details or None if the item is not found.
    :rtype: dict or None

    :raises: Exception if an error occurs during the database operation.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM inventory WHERE name = ?', (item_name,))
        row = cur.fetchone()

        if row:
            item = dict(row)
            return item
        else:
            return None

    except Exception as e:
        print(f"Error getting item by name: {e}")
    finally:
        conn.close()

def update_item(item_id, updates):
    """
    Updates an item in the 'inventory' table.

    :param item_id: The unique identifier for the item to be updated.
    :type item_id: int

    :param updates: A dictionary containing the fields to be updated and their new values.
    :type updates: dict

    :return: A dictionary containing the updated item's details or an error message.
    :rtype: dict

    :raises: Exception if an error occurs during the database operation.
    """
    updated_item = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        update_query = "UPDATE inventory SET "
        update_values = []

        for key, value in updates.items():
            update_query += f"{key} = ?, "
            update_values.append(value)

        update_query = update_query.rstrip(', ')
        update_query += f" WHERE item_id = {item_id}"

        cur.execute(update_query, tuple(update_values))
        conn.commit()
        updated_item = get_item_by_id(item_id)

    except Exception as e:
        conn.rollback()
        updated_item = {"error": f"Error updating item: {e}"}
    finally:
        conn.close()

    return updated_item

def deduce_item_from_stock(item_id, quantity):
    """
    Deducts a specified quantity from the item's stock.

    :param item_id: The unique identifier for the item.
    :type item_id: int

    :param quantity: The quantity to be deducted from the item's stock.
    :type quantity: int

    :return: A dictionary containing the updated item's details or an error message.
    :rtype: dict

    :raises: Exception if an error occurs during the database operation.
    """
    updated_item = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE inventory SET count_in_stock = count_in_stock - ? WHERE item_id = ?", (quantity, item_id))
        conn.commit()
        updated_item = get_item_by_id(item_id)
    except Exception as e:
        conn.rollback()
        updated_item = {"error": f"Error deducing item from stock: {e}"}
    finally:
        conn.close()

    return updated_item
