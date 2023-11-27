import sqlite3

def connect_to_db():
    conn = sqlite3.connect('ecommerce.db')
    return conn

def create_customers_table():
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
    except sqlite3.IntegrityError:
        conn.rollback()
        inserted_customer = {"error": "Username is already taken. Please choose another username."}
    except Exception as e:
        conn.rollback()
        inserted_customer = {"error": f"Error inserting customer: {e}"}
    finally:
        conn.close()
    return inserted_customer

def get_all_customers():
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
    updated_customer = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        update_query = "UPDATE customers SET "
        update_values = []

        for key, value in updates.items():
            update_query += f"{key} = ?, "
            update_values.append(value)

        update_query = update_query.rstrip(', ')
        update_query += f" WHERE customer_id = {customer_id}"

        cur.execute(update_query, tuple(update_values))
        conn.commit()
        updated_customer = get_customer_by_id(customer_id)

    except Exception as e:
        conn.rollback()
        updated_customer = {"error": f"Error updating customer: {e}"}
    finally:
        conn.close()

    return updated_customer

def delete_customer(customer_id):
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
