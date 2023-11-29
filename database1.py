"""
Module that contains functions for connecting to and managing an SQLite3 database for an ecommerce service.
"""

import sqlite3

def connect_to_db():
    """
    Establishes a connection to the SQLite3 database 'ecommerce_customers.db'.

    :return: The established connection object.
    :rtype: sqlite3.Connection
    """
    conn = sqlite3.connect('ecommerce_customers.db')
    return conn

def create_customers_table():
    """
    Creates a table named 'customers' in the SQLite3 database if it does not already exist.

    The table contains columns for the customer's id, full name, username, password, age, address, gender, marital status, and wallet balance.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                age INTEGER,
                address TEXT,
                gender TEXT,
                marital_status TEXT,
                wallet_balance REAL DEFAULT 0); 
                ''')
        conn.commit()
        print("Customers table created successfully")
    except Exception as e:
        print(f"Error creating customers table: {e}")
    finally:
        conn.close()

def insert_customer(customer):
    """
    Inserts a new customer record into the 'customers' table.

    :param customer: A dictionary containing the customer's details.
                     Required keys: 'full_name', 'username', 'password', 'age', 'address', 'gender', 'marital_status'
    :type customer: dict
    :return: A dictionary containing the inserted customer's details or an error message.
    :rtype: dict
    """
    inserted_customer = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO customers (full_name, username, password, age, address, gender, marital_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
            (customer['full_name'],
            customer['username'],
            customer['password'],
            customer['age'],
            customer['address'],
            customer['gender'],
            customer['marital_status']
        ))
        conn.commit()
        inserted_customer = get_customer_by_username(customer['username'])
        inserted_customer['customer_id'] = inserted_customer.get('customer_id')
        if 'customer_id' not in inserted_customer or inserted_customer['customer_id'] is None:
            raise ValueError("Failed to retrieve valid customer_id after insertion.")
         

    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise e
    except Exception as e:
        conn.rollback()
        inserted_customer = {"error": f"Error inserting customer: {e}"}
    finally:
        conn.close()

    return inserted_customer

def get_all_customers():
    """
    Retrieves all customer records from the 'customers' table.

    :return: A list of dictionaries containing the details of all customers.
    :rtype: list
    """
    customers = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers")
        rows = cur.fetchall()

        for row in rows:
            customer = dict(row)
            customers.append(customer)

    except Exception as e:
        print(f"Error getting all customers: {e}")
    finally:
        conn.close()

    return customers

def get_customer_by_username(username):
    """
    Retrieves a customer record from the 'customers' table based on the provided username.

    :param username: The username of the customer to retrieve.
    :type username: str
    :return: A dictionary containing the details of the customer with the provided username, or an empty dictionary if not found.
    :rtype: dict
    """
    customer = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers WHERE username = ?", (username,))
        row = cur.fetchone()

        if row:
            customer = dict(row)

    except Exception as e:
        print(f"Error getting customer by username: {e}")
    finally:
        conn.close()

    return customer

def update_customer(customer_id, updates):
    """
    Updates a customer record in the 'customers' table with the provided changes.

    :param customer_id: The ID of the customer to update.
    :type customer_id: int
    :param updates: A dictionary containing the fields to update and their new values.
    :type updates: dict
    :return: A dictionary containing the updated customer's details or an error message.
    :rtype: dict
    """
    updated_customer = {}
    try:
        if customer_id is None:
            raise ValueError("customer_id cannot be None.")
        conn = connect_to_db()
        cur = conn.cursor()
        update_query = "UPDATE customers SET "
        update_values = []

        if not updates:
            raise ValueError("No updates provided.")

        for key, value in updates.items():
            update_query += f"{key} = ?, "
            update_values.append(value)

        update_query = update_query.rstrip(', ')
        update_query += " WHERE customer_id = ?;"
        update_values.append(customer_id)

        print("Executing query:", update_query)
        print("Values:", update_values)


        cur.execute(update_query, tuple(update_values))
        conn.commit()
        updated_customer = get_customer_by_id(customer_id)
        print("Updated customer:", updated_customer)

    except Exception as e:
        conn.rollback()
        updated_customer = {"error": f"Error updating customer: {e}"}
    finally:
        conn.close()

    return updated_customer

def delete_customer(customer_id):
    """
    Deletes a customer record from the 'customers' table.

    :param customer_id: The ID of the customer to delete.
    :type customer_id: int
    :return: A dictionary containing a status message indicating whether the deletion was successful or an error message.
    :rtype: dict
    """
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
        conn.commit()
        message["status"] = "Customer deleted successfully"
    except Exception as e:
        conn.rollback()
        message["status"] = f"Cannot delete customer: {e}"
    finally:
        conn.close()

    return message

def charge_customer_wallet(customer_id, amount):
    """
    Adds the specified amount to a customer's wallet balance.

    :param customer_id: The ID of the customer.
    :type customer_id: int
    :param amount: The amount to add to the customer's wallet balance.
    :type amount: float
    :return: A dictionary containing the updated customer's details or an error message.
    :rtype: dict
    """
    updated_customer = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE customers SET wallet_balance = wallet_balance + ? WHERE customer_id = ?", (amount, customer_id))
        conn.commit()
        updated_customer = get_customer_by_id(customer_id)
    except Exception as e:
        conn.rollback()
        updated_customer = {"error": f"Error charging customer wallet: {e}"}
    finally:
        conn.close()

    return updated_customer

def deduce_money_from_wallet(customer_id, amount):
    """
    Deducts the specified amount from a customer's wallet balance.

    :param customer_id: The ID of the customer.
    :type customer_id: int
    :param amount: The amount to deduct from the customer's wallet balance.
    :type amount: float
    :return: A dictionary containing the updated customer's details or an error message.
    :rtype: dict
    """
    updated_customer = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE customers SET wallet_balance = wallet_balance - ? WHERE customer_id = ?", (amount, customer_id))
        conn.commit()
        updated_customer = get_customer_by_id(customer_id)
    except Exception as e:
        conn.rollback()
        updated_customer = {"error": f"Error deducing money from customer wallet: {e}"}
    finally:
        conn.close()

    return updated_customer

def get_customer_by_id(customer_id):
    """
    Retrieves a customer record from the 'customers' table based on the provided customer ID.

    :param customer_id: The ID of the customer to retrieve.
    :type customer_id: int
    :return: A dictionary containing the details of the customer with the provided ID, or an empty dictionary if not found.
    :rtype: dict
    """
    customer = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
        row = cur.fetchone()

        if row:
            customer = dict(row)

    except Exception as e:
        print(f"Error getting customer by ID: {e}")
    finally:
        conn.close()

    return customer
