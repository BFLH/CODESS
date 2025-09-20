import database
import sqlite3  #modelo de importacion de la base de datos

def add_new_client(cedula, nombre, apellido, telefono, email):
    conn = database.connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Clientes (cedula, nombre, apellido, telefono, email) VALUES (?, ?, ?, ?, ?)",
                       (cedula, nombre, apellido, telefono, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # print("Cédula ya registrada.") # Quitar print, la UI manejará el mensaje
        return False
    finally:
        conn.close()

def get_client_info(cedula=None, client_id=None):
    conn = database.connect_db()
    cursor = conn.cursor()
    if cedula:
        cursor.execute("SELECT * FROM Clientes WHERE cedula = ?", (cedula,))
    elif client_id:
        cursor.execute("SELECT * FROM Clientes WHERE id = ?", (client_id,))
    client = cursor.fetchone()
    conn.close()
    return client

def get_all_clients():
    """Obtiene todos los clientes registrados."""
    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, cedula, nombre, apellido, telefono, email FROM Clientes ORDER BY nombre, apellido")
    clients = cursor.fetchall()
    conn.close()
    return clients