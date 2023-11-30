"""
Module that contains functions for connecting to and managing an SQLite3 database for recording sales in an ecommerce platform.
"""

import sqlite3
from database2 import connect_to_dbi

def connect_to_db():
    """
    Establishes a connection to the database 'ecommerce_sales.db'.
    
    :return: The established connection object.
    :rtype: sqlite3.Connection
    """
    conn = sqlite3.connect('ecommerce_sales.db')
    return conn

def create_sales_table():
    """
    Creates a table named 'sales' in the database if it does not already exist.

    The table contains columns for sale_id, customer_id, item_id, sale_date, with foreign key constraints.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                item_id INTEGER,
                sale_date TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (item_id) REFERENCES inventory(item_id)
            );
        ''')
        conn.commit()
        print("Sales table created successfully")
    except Exception as e:
        print(f"Error creating sales table: {e}")
    finally:
        conn.close()

def make_sale(customer_id, item_id):
    """
    Records a sale in the 'sales' table.

    :param customer_id: The unique identifier for the customer making the sale.
    :type customer_id: int

    :param item_id: The unique identifier for the item being sold.
    :type item_id: int

    :raises: Exception if an error occurs during the database operation.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO sales (customer_id, item_id, sale_date)
            VALUES (?, ?, datetime('now'))
        ''', (customer_id, item_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error making sale: {e}")
    finally:
        conn.close()

def get_customer_sales(customer_id):
    """
    Retrieves sales made by a specific customer.

    :param customer_id: The unique identifier for the customer.
    :type customer_id: int

    :return: A list of dictionaries, where each dictionary represents a sale with sale_id, sale_date,
             item_name, and price_per_item details.
    :rtype: list

    :raises: Exception if an error occurs during the database operation.
    """
    sales = []
    try:
        conn_sales = connect_to_db()
        conn_sales.row_factory = sqlite3.Row
        cur_sales = conn_sales.cursor()
        cur_sales.execute('''
            SELECT sales.sale_id, sales.sale_date, sales.item_id
            FROM sales
            WHERE sales.customer_id = ?
        ''', (customer_id,))
        rows_sales = cur_sales.fetchall()

        conn_inventory = connect_to_dbi()
        conn_inventory.row_factory = sqlite3.Row
        cur_inventory = conn_inventory.cursor()

        for row_sales in rows_sales:
            cur_inventory.execute('''
                SELECT inventory.name, inventory.price_per_item
                FROM inventory
                WHERE inventory.item_id = ?
            ''', (row_sales['item_id'],))
            row_inventory = cur_inventory.fetchone()

            sale = {
                'sale_id': row_sales['sale_id'],
                'sale_date': row_sales['sale_date'],
                'item_name': row_inventory['name'],
                'price_per_item': row_inventory['price_per_item']
            }
            sales.append(sale)

    except Exception as e:
        print(f"Error getting customer sales: {e}")
    finally:
        conn_sales.close()
        conn_inventory.close()

    return sales
