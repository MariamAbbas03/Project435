import sqlite3

def connect_to_db():
    conn = sqlite3.connect('ecommerce_inventory.db')
    return conn

def create_inventory_table():
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

def update_item(item_id, updates):
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
