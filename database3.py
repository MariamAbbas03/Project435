import sqlite3

def connect_to_db():
    conn = sqlite3.connect('ecommerce_sales.db')
    return conn

def create_sales_table():
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
    sales = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('''
            SELECT sales.sale_id, sales.sale_date, inventory.name, inventory.price_per_item
            FROM sales
            JOIN inventory ON sales.item_id = inventory.item_id
            WHERE sales.customer_id = ?
        ''', (customer_id,))
        rows = cur.fetchall()

        for row in rows:
            sale = dict(row)
            sales.append(sale)

    except Exception as e:
        print(f"Error getting customer sales: {e}")
    finally:
        conn.close()

    return sales
