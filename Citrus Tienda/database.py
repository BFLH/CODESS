# database.py
import sqlite3
import hashlib
import time

def connect_db():
    """Conecta a la base de datos SQLite 'citrus_tech.db'."""
    conn = sqlite3.connect('citrus_tech.db')
    return conn

def setup_database():
    """Crea las tablas necesarias si no existen y añade un usuario admin por defecto."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('Gerente', 'Trabajador'))
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        sku TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        total_amount REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sale_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER NOT NULL,
        product_sku TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price_at_sale REAL NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES sales (id),
        FOREIGN KEY (product_sku) REFERENCES products (sku)
    )''')
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if cursor.fetchone() is None:
        hashed_password = hashlib.sha256('admin'.encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                        ('admin', hashed_password, 'Gerente'))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT id, role FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user

def generate_sku(product_name):
    """Genera un SKU con prefijo temático 'CT'."""
    prefix = product_name[:3].upper().strip()
    timestamp = str(int(time.time()))[-6:]
    return f"CT-{prefix}-{timestamp}"

def add_user(username, password, role):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError: return False
    finally: conn.close()

def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def update_user(user_id, username, password, role):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        if password:  # Si se proporciona una nueva contraseña
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                "UPDATE users SET username = ?, password = ?, role = ? WHERE id = ?",
                (username, hashed_password, role, user_id)
            )
        else:  # Si no se proporciona contraseña, no la actualices
            cursor.execute(
                "UPDATE users SET username = ?, role = ? WHERE id = ?",
                (username, role, user_id)
            )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def add_product(name, price, stock):
    conn = connect_db()
    cursor = conn.cursor()
    sku = generate_sku(name)
    cursor.execute("INSERT INTO products (sku, name, price, stock) VALUES (?, ?, ?, ?)", (sku, name, price, stock))
    conn.commit()
    conn.close()

def get_all_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sku, name, price, stock FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def update_product(sku, name, price, stock):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = ?, price = ?, stock = ? WHERE sku = ?", (name, price, stock, sku))
    conn.commit()
    conn.close()
    
def delete_product(sku):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE sku = ?", (sku,))
    conn.commit()
    conn.close()

def record_sale(user_id, cart, client_name, client_id, client_phone):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        total_amount = sum(item['price'] * item['quantity'] for item in cart)
        cursor.execute(
            "INSERT INTO sales (user_id, total_amount, client_name, client_id, client_phone) VALUES (?, ?, ?, ?, ?)",
            (user_id, total_amount, client_name, client_id, client_phone)
        )
        sale_id = cursor.lastrowid
        for item in cart:
            cursor.execute("INSERT INTO sale_details (sale_id, product_sku, quantity, price_at_sale) VALUES (?, ?, ?, ?)",
                           (sale_id, item['sku'], item['quantity'], item['price']))
            cursor.execute("UPDATE products SET stock = stock - ? WHERE sku = ?", 
                            (item['quantity'], item['sku']))
        conn.commit()
        return sale_id, total_amount
    except Exception as e:
        conn.rollback()
        print(f"Error al registrar la venta: {e}")
        return None, None
    finally:
        conn.close()

def get_sales_history():
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        SELECT s.id, u.username, s.total_amount, s.timestamp, s.client_name, s.client_id, s.client_phone
        FROM sales s
        JOIN users u ON s.user_id = u.id
        ORDER BY s.timestamp DESC
    """
    cursor.execute(query)
    history = cursor.fetchall()
    conn.close()
    return history