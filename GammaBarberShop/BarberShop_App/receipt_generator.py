import os
import datetime
from fpdf import FPDF
import database


def generate_receipt_pdf(invoice_id, output_folder="Recibos"):
    """
    Genera un recibo en PDF para una factura dada y lo guarda en la carpeta especificada.
    """
    # Asegurarse de que la carpeta de salida exista
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    conn = database.connect_db()
    cursor = conn.cursor()
    invoice_data = None
    try:
        cursor.execute("""
            SELECT
                F.id, F.fecha_emision, F.total, F.metodo_pago,
                C.fecha_cita, C.hora_cita, C.servicio, C.precio,
                CL.nombre, CL.apellido, CL.cedula, CL.telefono, CL.email
            FROM Facturas AS F
            JOIN Citas AS C ON F.cita_id = C.id
            JOIN Clientes AS CL ON C.cliente_id = CL.id
            WHERE F.id = ?
        """, (invoice_id,))
        invoice_data = cursor.fetchone()
    except Exception as e:
        conn.close()
        return False, f"Error al consultar la base de datos: {e}"
    finally:
        conn.close()

    if not invoice_data:
        return False, f"Factura {invoice_id} no encontrada."

    (
        factura_id, fecha_emision, total, metodo_pago,
        fecha_cita, hora_cita, servicio_cita, precio_cita,
        nombre_cliente, apellido_cliente, cedula_cliente, telefono_cliente, email_cliente
    ) = invoice_data

    # Formatear la fecha para el nombre del archivo
    receipt_date_str = datetime.datetime.strptime(fecha_emision, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_folder, f"recibo_factura_{factura_id}_{receipt_date_str}.pdf")

    # Inicializar FPDF
    pdf = FPDF()
    pdf.add_page()
    # usa fuente  arial
    pdf.set_font("Arial", size=12)

    # Título del recibo
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Recibo de BarberShop", ln=True, align='C')
    pdf.ln(10)

    # Información de la factura
    pdf.set_font("Arial", '', 12)
    pdf.write(5, f"Factura #: {factura_id} \n")
    pdf.write(5, f"Fecha de Emisión: {fecha_emision} \n")
    pdf.write(5, f"Método de Pago: {metodo_pago} \n")
    pdf.ln(10)

    # Información del cliente
    pdf.set_font("Arial", 'B', 14)  # Corrige "Anrial" por "Arial"
    pdf.write(5, "Información del Cliente:\n")
    pdf.set_font("Arial", '', 12)
    pdf.write(5, f"Nombre: {nombre_cliente} {apellido_cliente}\n")
    pdf.write(5, f"Cédula: {cedula_cliente if cedula_cliente else 'N/A'}\n")
    pdf.write(5, f"Teléfono: {telefono_cliente if telefono_cliente else 'N/A'}\n")
    pdf.write(5, f"Email: {email_cliente if email_cliente else 'N/A'}\n")
    pdf.ln(10)

    # Detalles del Servicio/Cita (Tabla simple con celdas)
    pdf.set_font("Arial", 'B', 14)
    pdf.write(5, "Detalles del Servicio:\n")
    pdf.ln(2)

    # Encabezados de tabla
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, "Servicio", 1, 0, 'C')
    pdf.cell(40, 10, "Fecha Cita", 1, 0, 'C')
    pdf.cell(30, 10, "Hora Cita", 1, 0, 'C')
    pdf.cell(40, 10, "Precio (USD)", 1, True, 'C')

    # Datos de la tabla
    pdf.set_font("Arial", '', 12)
    pdf.cell(50, 10, servicio_cita if servicio_cita else 'N/A', 1, 0, 'C')
    pdf.cell(40, 10, fecha_cita if fecha_cita else 'N/A', 1, 0, 'C')
    pdf.cell(30, 10, hora_cita if hora_cita else 'N/A', 1, 0, 'C')
    precio_cita = precio_cita if precio_cita is not None else 0.0
    pdf.cell(40, 10, f"${precio_cita:.2f}", 1, True, 'C')
    pdf.ln(10)

    # Total
    pdf.set_font("Arial", 'B', 16)
    total = total if total is not None else 0.0
    pdf.cell(200, 10, f"Total Pagado: ${total:.2f} USD", ln=True, align='R')
    pdf.ln(20)

    # Mensaje de agradecimiento
    pdf.set_font("Helvetica", 'I', 12)
    pdf.cell(200, 10, "¡Gracias por su visita a BarberShop!", ln=True, align='C')

    try:
        pdf.output(filename)
        return True, filename
    except Exception as e:
        return False, f"Error al generar PDF: {e}"

