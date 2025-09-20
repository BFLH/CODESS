import database
import datetime

def schedule_new_appointment(client_id, date_str, time_str, service, price):
    conn = database.connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Citas (cliente_id, fecha_cita, hora_cita, servicio, precio, estado) VALUES (?, ?, ?, ?, ?, ?)",
                       (client_id, date_str, time_str, service, price, 'Pendiente'))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al agendar cita: {e}")
        return False
    finally:
        conn.close()

def get_appointments_for_date(date_str):
    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Citas.id, Clientes.nombre, Clientes.apellido, Citas.hora_cita, Citas.servicio, Citas.precio, Citas.estado
        FROM Citas JOIN Clientes ON Citas.cliente_id = Clientes.id
        WHERE Citas.fecha_cita = ? ORDER BY Citas.hora_cita
    """, (date_str,))
    appointments = cursor.fetchall()
    conn.close()
    return appointments

def update_appointment_status(appointment_id, new_status):
    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Citas SET estado = ? WHERE id = ?", (new_status, appointment_id))
    conn.commit()
    conn.close()

def get_appointment_details(appointment_id):
    conn = database.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Citas WHERE id = ?", (appointment_id,))
    details = cursor.fetchone()
    conn.close()
    return details
