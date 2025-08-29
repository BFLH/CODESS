# receipt.py
from fpdf import FPDF
import datetime
import os
import sys
import subprocess

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Citrus Tech - Comprobante de Venta', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def generate_receipt(sale_id, cart, total_amount, user_name, client_name=None, client_id=None, client_phone=None):
    pdf = PDF()
    pdf.add_page()
    # Intentar agregar el logo, pero continuar si falla
    try:
        pdf.image("C:\\Users\\USUARIO\\Downloads\\Citrus Tienda\\logo_citrus.jpg", 160, 8, 33)
    except Exception as e:
        print(f"Advertencia: No se pudo cargar el logo. {e}")
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, f'Comprobante No: {sale_id}', 0, 1, 'L')
    pdf.cell(0, 8, f'Fecha: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'L')
    pdf.cell(0, 8, f'Vendedor: {user_name}', 0, 1, 'L')
    # Mostrar datos del cliente si existen
    if client_name:
        pdf.cell(0, 8, f'Cliente: {client_name}', 0, 1, 'L')
    if client_id:
        pdf.cell(0, 8, f'Cédula: {client_id}', 0, 1, 'L')
    if client_phone:
        pdf.cell(0, 8, f'Teléfono: {client_phone}', 0, 1, 'L')
    pdf.ln(8)

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(80, 10, 'Producto', 1, 0, 'C')
    pdf.cell(30, 10, 'Cantidad', 1, 0, 'C')
    pdf.cell(40, 10, 'Precio Unit.', 1, 0, 'C')
    pdf.cell(40, 10, 'Subtotal', 1, 1, 'C')

    pdf.set_font('Arial', '', 10)
    for item in cart:
        subtotal = item['quantity'] * item['price']
        pdf.cell(80, 10, item['name'], 1, 0, 'L')
        pdf.cell(30, 10, str(item['quantity']), 1, 0, 'C')
        pdf.cell(40, 10, f'${item["price"]:.2f}', 1, 0, 'R')
        pdf.cell(40, 10, f'${subtotal:.2f}', 1, 1, 'R')
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(150, 12, 'TOTAL:', 0, 0, 'R')
    pdf.cell(40, 12, f'${total_amount:.2f}', 1, 1, 'R')
    
    pdf.ln(20)
    pdf.set_font('Arial', 'I', 12)
    pdf.cell(0, 10, '¡Gracias por elegir Citrus Tech!', 0, 1, 'C')

    if not os.path.exists('recibos_citrus_tech'):
        os.makedirs('recibos_citrus_tech')
        
    filename = f"recibos_citrus_tech/recibo_{sale_id}.pdf"
    pdf.output(filename)
    
    try:
        if sys.platform == "win32":
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])
    except Exception as e:
        print(f"No se pudo abrir el PDF automaticamente: {e}")