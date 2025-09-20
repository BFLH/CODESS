import sqlite3

DATABASE_NAME = 'barbershop.db'

def connect_db():
    return sqlite3.connect(DATABASE_NAME)

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    # Crear tablas si no existen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT UNIQUE,
            nombre TEXT NOT NULL,
            apellido TEXT,
            telefono TEXT,
            email TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            fecha_cita TEXT NOT NULL,
            hora_cita TEXT NOT NULL,
            servicio TEXT NOT NULL,
            precio REAL NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES Clientes(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cita_id INTEGER NOT NULL,
            fecha_emision TEXT NOT NULL,
            total REAL NOT NULL,
            metodo_pago TEXT,
            FOREIGN KEY (cita_id) REFERENCES Citas(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(usuario, contrasena, rol='barbero'):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Usuarios (usuario, contrasena, rol) VALUES (?, ?, ?)",
                       (usuario, contrasena, rol))
        conn.commit()
        print(f"Usuario '{usuario}' añadido.")
    except sqlite3.IntegrityError:
        print(f"El usuario '{usuario}' ya existe.")
    finally:
        conn.close()

# Función para obtener un usuario por nombre de usuario
def get_user_by_username(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE usuario = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user
