    
import database
import datetime
# Ya no necesitamos importar fpdf aquí

def process_payment(appointment_id, method_of_payment):
    conn = database.connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Citas WHERE id = ?", (appointment_id,))
    appointment_details = cursor.fetchone()
    if not appointment_details:
        conn.close()
        return False, "Cita no encontrada.", None # Añadir None para invoice_id

    cita_id, cliente_id, fecha_cita, hora_cita, servicio, precio, estado = appointment_details

    fecha_emision = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    invoice_id = None # Inicializar invoice_id
    try:
        cursor.execute("INSERT INTO Facturas (cita_id, fecha_emision, total, metodo_pago) VALUES (?, ?, ?, ?)",
                       (cita_id, fecha_emision, precio, method_of_payment))
        conn.commit()

        # Obtener el ID de la factura recién creada
        invoice_id = cursor.lastrowid

        cursor.execute("UPDATE Citas SET estado = 'Completada' WHERE id = ?", (appointment_id,))
        conn.commit()
        return True, "Pago procesado y factura registrada.", invoice_id
    except Exception as e:
        conn.rollback()
        return False, f"Error al procesar el pago: {e}", None
    finally:
        conn.close()

# La función generate_receipt_pdf se ha movido a receipt_generator.py

  