import database

def verify_login(username, password):
    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE usuario = ? AND contrasena = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None, user
