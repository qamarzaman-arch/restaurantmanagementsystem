import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

class DatabaseManager:
    def __init__(self, db_path="restaurant.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    full_name TEXT
                )
            ''')

            # Settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')

            # Categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            ''')

            # Menu items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    description TEXT,
                    available INTEGER DEFAULT 1,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            ''')

            # Tables table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS restaurant_tables (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_number TEXT UNIQUE NOT NULL,
                    capacity INTEGER,
                    status TEXT DEFAULT 'Available'
                )
            ''')

            # Orders table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_id INTEGER,
                    order_type TEXT, -- Dine-in, Takeaway, Delivery
                    status TEXT DEFAULT 'Pending', -- Pending, Completed, Cancelled
                    subtotal REAL DEFAULT 0,
                    tax REAL DEFAULT 0,
                    discount REAL DEFAULT 0,
                    total REAL DEFAULT 0,
                    payment_method TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (table_id) REFERENCES restaurant_tables (id)
                )
            ''')

            # Order items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER,
                    menu_item_id INTEGER,
                    quantity INTEGER,
                    price REAL,
                    FOREIGN KEY (order_id) REFERENCES orders (id),
                    FOREIGN KEY (menu_item_id) REFERENCES menu_items (id)
                )
            ''')

            # Inventory table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT UNIQUE NOT NULL,
                    quantity REAL DEFAULT 0,
                    unit TEXT,
                    min_threshold REAL DEFAULT 0
                )
            ''')

            # Customers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT UNIQUE,
                    email TEXT,
                    points INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()

            # Seed default admin if not exists
            self.add_user("admin", "admin123", "Admin", "System Administrator")

            # Seed default settings
            self.set_setting("restaurant_name", "Gourmet Restaurant")
            self.set_setting("tax_rate", "5.0")

    # User Management
    def add_user(self, username, password, role, full_name=""):
        hashed_pw = generate_password_hash(password)
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                    (username, hashed_pw, role, full_name)
                )
                return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        with self.get_connection() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if user and check_password_hash(user['password'], password):
                return dict(user)
        return None

    # Settings Management
    def set_setting(self, key, value):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, str(value))
            )

    def get_setting(self, key, default=None):
        with self.get_connection() as conn:
            res = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
            return res['value'] if res else default

    def get_all_settings(self):
        with self.get_connection() as conn:
            res = conn.execute("SELECT * FROM settings").fetchall()
            return {row['key']: row['value'] for row in res}

    # Categories
    def add_category(self, name):
        try:
            with self.get_connection() as conn:
                conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
                return True
        except sqlite3.IntegrityError:
            return False

    def get_categories(self):
        with self.get_connection() as conn:
            return [dict(row) for row in conn.execute("SELECT * FROM categories").fetchall()]

    def delete_category(self, cat_id):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM categories WHERE id = ?", (cat_id,))

    # Menu Items
    def add_menu_item(self, category_id, name, price, description="", available=1):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO menu_items (category_id, name, price, description, available) VALUES (?, ?, ?, ?, ?)",
                (category_id, name, price, description, available)
            )

    def get_menu_items(self, category_id=None):
        query = "SELECT m.*, c.name as category_name FROM menu_items m JOIN categories c ON m.category_id = c.id"
        params = []
        if category_id:
            query += " WHERE m.category_id = ?"
            params.append(category_id)
        with self.get_connection() as conn:
            return [dict(row) for row in conn.execute(query, params).fetchall()]

    def update_menu_item(self, item_id, **kwargs):
        cols = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        params = list(kwargs.values()) + [item_id]
        with self.get_connection() as conn:
            conn.execute(f"UPDATE menu_items SET {cols} WHERE id = ?", params)

    def delete_menu_item(self, item_id):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM menu_items WHERE id = ?", (item_id,))

    # Tables
    def add_table(self, table_number, capacity):
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "INSERT INTO restaurant_tables (table_number, capacity) VALUES (?, ?)",
                    (table_number, capacity)
                )
                return True
        except sqlite3.IntegrityError:
            return False

    def get_tables(self):
        with self.get_connection() as conn:
            return [dict(row) for row in conn.execute("SELECT * FROM restaurant_tables").fetchall()]

    def update_table_status(self, table_id, status):
        with self.get_connection() as conn:
            conn.execute("UPDATE restaurant_tables SET status = ? WHERE id = ?", (status, table_id))

    # Orders
    def create_order(self, table_id, order_type):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO orders (table_id, order_type) VALUES (?, ?)",
                (table_id, order_type)
            )
            order_id = cursor.lastrowid
            if table_id:
                cursor.execute("UPDATE restaurant_tables SET status = 'Occupied' WHERE id = ?", (table_id,))
            return order_id

    def add_order_item(self, order_id, menu_item_id, quantity, price):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO order_items (order_id, menu_item_id, quantity, price) VALUES (?, ?, ?, ?)",
                (order_id, menu_item_id, quantity, price)
            )

    def get_order(self, order_id):
        with self.get_connection() as conn:
            order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
            if not order: return None
            items = conn.execute(
                "SELECT oi.*, m.name FROM order_items oi JOIN menu_items m ON oi.menu_item_id = m.id WHERE oi.order_id = ?",
                (order_id,)
            ).fetchall()
            order_dict = dict(order)
            order_dict['items'] = [dict(i) for i in items]
            return order_dict

    def update_order_payment(self, order_id, subtotal, tax, discount, total, payment_method):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE orders SET
                subtotal = ?, tax = ?, discount = ?, total = ?,
                payment_method = ?, status = 'Completed'
                WHERE id = ?
            ''', (subtotal, tax, discount, total, payment_method, order_id))

            # Free the table
            order = conn.execute("SELECT table_id FROM orders WHERE id = ?", (order_id,)).fetchone()
            if order and order['table_id']:
                cursor.execute("UPDATE restaurant_tables SET status = 'Available' WHERE id = ?", (order['table_id'],))

    def get_all_orders(self, status=None, date_from=None, date_to=None):
        query = "SELECT * FROM orders WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if date_from:
            query += " AND created_at >= ?"
            params.append(f"{date_from} 00:00:00")
        if date_to:
            query += " AND created_at <= ?"
            params.append(f"{date_to} 23:59:59")

        query += " ORDER BY created_at DESC"
        with self.get_connection() as conn:
            return [dict(row) for row in conn.execute(query, params).fetchall()]

    # Inventory
    def update_inventory(self, item_name, quantity_change, unit=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            res = cursor.execute("SELECT quantity FROM inventory WHERE item_name = ?", (item_name,)).fetchone()
            if res:
                new_qty = res['quantity'] + quantity_change
                cursor.execute("UPDATE inventory SET quantity = ? WHERE item_name = ?", (new_qty, item_name))
            else:
                cursor.execute(
                    "INSERT INTO inventory (item_name, quantity, unit) VALUES (?, ?, ?)",
                    (item_name, quantity_change, unit)
                )

    def get_inventory(self):
        with self.get_connection() as conn:
            return [dict(row) for row in conn.execute("SELECT * FROM inventory").fetchall()]

    # Customers
    def add_customer(self, name, phone, email=""):
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)",
                    (name, phone, email)
                )
                return True
        except sqlite3.IntegrityError:
            return False

    def get_customers(self):
        with self.get_connection() as conn:
            return [dict(row) for row in conn.execute("SELECT * FROM customers").fetchall()]

    def update_customer(self, cust_id, **kwargs):
        cols = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        params = list(kwargs.values()) + [cust_id]
        with self.get_connection() as conn:
            conn.execute(f"UPDATE customers SET {cols} WHERE id = ?", params)

    # Insights
    def get_sales_by_category(self):
        query = """
            SELECT c.name, SUM(oi.quantity * oi.price) as total_sales
            FROM categories c
            JOIN menu_items m ON c.id = m.category_id
            JOIN order_items oi ON m.id = oi.menu_item_id
            JOIN orders o ON oi.order_id = o.id
            WHERE o.status = 'Completed'
            GROUP BY c.name
        """
        with self.get_connection() as conn:
            return [dict(row) for row in conn.execute(query).fetchall()]

    def get_top_selling_items(self, limit=5):
        query = """
            SELECT m.name, SUM(oi.quantity) as total_qty
            FROM menu_items m
            JOIN order_items oi ON m.id = oi.menu_item_id
            JOIN orders o ON oi.order_id = o.id
            WHERE o.status = 'Completed'
            GROUP BY m.name
            ORDER BY total_qty DESC
            LIMIT ?
        """
        with self.get_connection() as conn:
            return [dict(row) for row in conn.execute(query, (limit,)).fetchall()]

    def get_weekly_sales_trend(self):
        query = """
            SELECT date(created_at) as sale_date, SUM(total) as daily_total
            FROM orders
            WHERE status = 'Completed' AND created_at >= date('now', '-7 days')
            GROUP BY sale_date
            ORDER BY sale_date ASC
        """
        with self.get_connection() as conn:
            return [dict(row) for row in conn.execute(query).fetchall()]
