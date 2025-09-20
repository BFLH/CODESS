import tkinter as tk
from tkinter import messagebox, ttk
import database, auth, client_manager, appointment_scheduler, billing_system
import receipt_generator 
import datetime
import re

class BarberShopApp:
    def __init__(self, master):
        self.master = master
        master.title("BarberShop - Gestión")
        master.geometry("1000x650")

        database.init_db()

        self.create_login_screen()

    def create_login_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.login_frame = tk.Frame(self.master, padx=20, pady=20)
        self.login_frame.pack(expand=True)

        tk.Label(self.login_frame, text="Usuario:", font=('Arial', 12)).pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame, font=('Arial', 12))
        self.username_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Contraseña:", font=('Arial', 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*", font=('Arial', 12))
        self.password_entry.pack(pady=5)

        tk.Button(self.login_frame, text="Iniciar Sesión", command=self.login, font=('Arial', 12)).pack(pady=15)

        conn = database.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE usuario = 'admin'")
        if not cursor.fetchone():
            database.add_user('admin', 'adminpass', 'admin')
        conn.close()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        logged_in, user_data = auth.verify_login(username, password)

        if logged_in:
            messagebox.showinfo("Login Exitoso", f"¡Bienvenido, {username}!")
            self.user_role = user_data[3]
            self.create_main_app_screen()
        else:
            messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")

    def create_main_app_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.clients_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.clients_frame, text="Clientes")
        self.setup_clients_tab()

        self.appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.appointments_frame, text="Agendar Cita")
        self.setup_appointments_tab()

        self.daily_appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.daily_appointments_frame, text="Citas del Día / Cobro")
        self.setup_daily_appointments_tab()

        if self.user_role == 'admin':
            self.reports_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.reports_frame, text="Reportes")
            # self.setup_reports_tab()

    def setup_clients_tab(self):
        add_client_frame = ttk.LabelFrame(self.clients_frame, text="Añadir Nuevo Cliente", padding=10)
        add_client_frame.pack(pady=10, padx=10, fill="x")

        validate_numeric = self.master.register(self.validate_numeric_input)
        validate_alphabetic = self.master.register(self.validate_alphabetic_input)
        validate_email = self.master.register(self.validate_email_input)

        tk.Label(add_client_frame, text="Cédula:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.client_cedula_entry = tk.Entry(add_client_frame, validate="key", validatecommand=(validate_numeric, '%P'))
        self.client_cedula_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(add_client_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.client_name_entry = tk.Entry(add_client_frame, validate="key", validatecommand=(validate_alphabetic, '%P'))
        self.client_name_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(add_client_frame, text="Apellido:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.client_lastname_entry = tk.Entry(add_client_frame, validate="key", validatecommand=(validate_alphabetic, '%P'))
        self.client_lastname_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(add_client_frame, text="Teléfono:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.client_phone_entry = tk.Entry(add_client_frame, validate="key", validatecommand=(validate_numeric, '%P'))
        self.client_phone_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(add_client_frame, text="Email:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.client_email_entry = tk.Entry(add_client_frame)
        self.client_email_entry.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        ttk.Button(add_client_frame, text="Guardar Cliente", command=self.add_client).grid(row=5, column=0, columnspan=2, pady=10)

        view_clients_frame = ttk.LabelFrame(self.clients_frame, text="Clientes Registrados", padding=10)
        view_clients_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.clients_tree = ttk.Treeview(view_clients_frame, columns=("ID", "Cédula", "Nombre", "Apellido", "Teléfono", "Email"), show="headings")
        self.clients_tree.heading("ID", text="ID")
        self.clients_tree.heading("Cédula", text="Cédula")
        self.clients_tree.heading("Nombre", text="Nombre")
        self.clients_tree.heading("Apellido", text="Apellido")
        self.clients_tree.heading("Teléfono", text="Teléfono")
        self.clients_tree.heading("Email", text="Email")

        self.clients_tree.column("ID", width=40, anchor="center")
        self.clients_tree.column("Cédula", width=100)
        self.clients_tree.column("Nombre", width=120)
        self.clients_tree.column("Apellido", width=120)
        self.clients_tree.column("Teléfono", width=100)
        self.clients_tree.column("Email", width=180)

        clients_scrollbar_y = ttk.Scrollbar(view_clients_frame, orient="vertical", command=self.clients_tree.yview)
        clients_scrollbar_x = ttk.Scrollbar(view_clients_frame, orient="horizontal", command=self.clients_tree.xview)
        self.clients_tree.configure(yscrollcommand=clients_scrollbar_y.set, xscrollcommand=clients_scrollbar_x.set)

        clients_scrollbar_y.pack(side="right", fill="y")
        clients_scrollbar_x.pack(side="bottom", fill="x")
        self.clients_tree.pack(fill="both", expand=True)

        self.load_clients_to_treeview()

    def validate_numeric_input(self, new_value):
        return new_value.isdigit() or new_value == ""

    def validate_alphabetic_input(self, new_value):
        return re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]*$", new_value) is not None

    def validate_email_input(self, email):
        return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None

    def add_client(self):
        cedula = self.client_cedula_entry.get().strip()
        nombre = self.client_name_entry.get().strip().title()
        apellido = self.client_lastname_entry.get().strip().title()
        telefono = self.client_phone_entry.get().strip()
        email = self.client_email_entry.get().strip()

        if not cedula or not nombre or not apellido:
            messagebox.showerror("Error de Validación", "Cédula, nombre y apellido son obligatorios.")
            return
        if not self.validate_numeric_input(cedula):
            messagebox.showerror("Error de Validación", "La cédula debe contener solo números.")
            return
        if telefono and not self.validate_numeric_input(telefono):
            messagebox.showerror("Error de Validación", "El teléfono debe contener solo números.")
            return
        if email and not self.validate_email_input(email):
            messagebox.showerror("Error de Validación", "Formato de email inválido.")
            return

        if client_manager.add_new_client(cedula, nombre, apellido, telefono, email):
            messagebox.showinfo("Éxito", "Cliente añadido exitosamente.")
            self.client_cedula_entry.delete(0, tk.END)
            self.client_name_entry.delete(0, tk.END)
            self.client_lastname_entry.delete(0, tk.END)
            self.client_phone_entry.delete(0, tk.END)
            self.client_email_entry.delete(0, tk.END)
            self.load_clients_to_treeview()
        else:
            messagebox.showerror("Error", "No se pudo añadir el cliente. La cédula podría estar duplicada.")

    def load_clients_to_treeview(self):
        for i in self.clients_tree.get_children():
            self.clients_tree.delete(i)

        clients = client_manager.get_all_clients()
        for client in clients:
            self.clients_tree.insert("", "end", values=client)

    def setup_appointments_tab(self):
        agendar_frame = ttk.LabelFrame(self.appointments_frame, text="Agendar Nueva Cita", padding=10)
        agendar_frame.pack(pady=10, padx=10, fill="x")

        validate_numeric = self.master.register(self.validate_numeric_input)
        validate_price = self.master.register(self.validate_price_input)

        tk.Label(agendar_frame, text="Cédula Cliente:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.appointment_cedula_entry = tk.Entry(agendar_frame, validate="key", validatecommand=(validate_numeric, '%P'))
        self.appointment_cedula_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        ttk.Button(agendar_frame, text="Buscar Cliente", command=self.search_client_for_appointment).grid(row=0, column=2, padx=5, pady=2)

        tk.Label(agendar_frame, text="Cliente Info:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.appointment_client_info = tk.Label(agendar_frame, text="Ningún cliente seleccionado", fg="blue")
        self.appointment_client_info.grid(row=1, column=1, columnspan=2, padx=5, pady=2, sticky="ew")
        self.selected_client_id = None

        tk.Label(agendar_frame, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.appointment_date_entry = tk.Entry(agendar_frame)
        self.appointment_date_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        self.appointment_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        tk.Label(agendar_frame, text="Hora (HH:MM):").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.appointment_time_entry = tk.Entry(agendar_frame)
        self.appointment_time_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(agendar_frame, text="Servicio:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.appointment_service_entry = ttk.Combobox(agendar_frame, values=["Corte de Cabello", "Barba", "Corte + Barba", "Lavado", "Otro"])
        self.appointment_service_entry.grid(row=4, column=1, padx=5, pady=2, sticky="ew")
        self.appointment_service_entry.set("Corte de Cabello")

        tk.Label(agendar_frame, text="Precio (USD):").grid(row=5, column=0, padx=5, pady=2, sticky="w")
        self.appointment_price_entry = tk.Entry(agendar_frame, validate="key", validatecommand=(validate_price, '%P'))
        self.appointment_price_entry.grid(row=5, column=1, padx=5, pady=2, sticky="ew")
        self.appointment_price_entry.insert(0, "15.00")

        ttk.Button(agendar_frame, text="Agendar Cita", command=self.schedule_appointment).grid(row=6, column=0, columnspan=3, pady=10)

    def validate_price_input(self, new_value):
        if new_value == "":
            return True
        return re.match(r"^\d*\.?\d*$", new_value) is not None

    def search_client_for_appointment(self):
        cedula = self.appointment_cedula_entry.get().strip()
        if not cedula:
            messagebox.showerror("Error", "Ingrese una cédula para buscar al cliente.")
            return

        client = client_manager.get_client_info(cedula=cedula)
        if client:
            self.selected_client_id = client[0]
            self.appointment_client_info.config(text=f"Cliente: {client[2]} {client[3]} (ID: {client[0]})", fg="green")
        else:
            self.selected_client_id = None
            self.appointment_client_info.config(text="Cliente no encontrado. Por favor, regístrelo primero.", fg="red")
            messagebox.showerror("Error", "Cliente no encontrado. Verifique la cédula o regístrelo en la pestaña de Clientes.")

    def schedule_appointment(self):
        if not self.selected_client_id:
            messagebox.showerror("Error", "Primero debe seleccionar un cliente.")
            return

        date_str = self.appointment_date_entry.get().strip()
        time_str = self.appointment_time_entry.get().strip()
        service = self.appointment_service_entry.get().strip()
        price_str = self.appointment_price_entry.get().strip()

        if not date_str or not time_str or not service or not price_str:
            messagebox.showerror("Error de Validación", "Todos los campos de la cita son obligatorios.")
            return

        try:
            price = float(price_str)
            if price <= 0:
                messagebox.showerror("Error de Validación", "El precio debe ser un número positivo.")
                return
        except ValueError:
            messagebox.showerror("Error de Validación", "El precio debe ser un número válido.")
            return

        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error de Validación", "Formato de fecha (YYYY-MM-DD) inválido.")
            return
        try:
            datetime.datetime.strptime(time_str, "%H:%M")
        except ValueError:
            messagebox.showerror("Error de Validación", "Formato de hora (HH:MM) inválido.")
            return

        if appointment_scheduler.schedule_new_appointment(self.selected_client_id, date_str, time_str, service, price):
            messagebox.showinfo("Éxito", "Cita agendada exitosamente.")
            self.appointment_time_entry.delete(0, tk.END)
            self.appointment_cedula_entry.delete(0, tk.END)
            self.appointment_client_info.config(text="Ningún cliente seleccionado", fg="blue")
            self.selected_client_id = None
            self.load_daily_appointments()
        else:
            messagebox.showerror("Error", "No se pudo agendar la cita.")

    def setup_daily_appointments_tab(self):
        daily_frame = ttk.LabelFrame(self.daily_appointments_frame, text="Citas para Hoy", padding=10)
        daily_frame.pack(pady=10, padx=10, fill="both", expand=True)

        tk.Label(daily_frame, text="Fecha de Citas (YYYY-MM-DD):").pack(pady=5)
        self.daily_date_entry = tk.Entry(daily_frame)
        self.daily_date_entry.pack(pady=5)
        self.daily_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        ttk.Button(daily_frame, text="Ver Citas", command=self.load_daily_appointments).pack(pady=5)

        self.appointments_tree = ttk.Treeview(daily_frame, columns=("ID", "Cliente", "Hora", "Servicio", "Precio", "Estado"), show="headings")
        self.appointments_tree.heading("ID", text="ID")
        self.appointments_tree.heading("Cliente", text="Cliente")
        self.appointments_tree.heading("Hora", text="Hora")
        self.appointments_tree.heading("Servicio", text="Servicio")
        self.appointments_tree.heading("Precio", text="Precio (USD)")
        self.appointments_tree.heading("Estado", text="Estado")

        self.appointments_tree.column("ID", width=50, anchor="center")
        self.appointments_tree.column("Cliente", width=150)
        self.appointments_tree.column("Hora", width=80, anchor="center")
        self.appointments_tree.column("Servicio", width=120)
        self.appointments_tree.column("Precio", width=100, anchor="e")
        self.appointments_tree.column("Estado", width=100, anchor="center")

        appointments_scrollbar_y = ttk.Scrollbar(daily_frame, orient="vertical", command=self.appointments_tree.yview)
        appointments_scrollbar_x = ttk.Scrollbar(daily_frame, orient="horizontal", command=self.appointments_tree.xview)
        self.appointments_tree.configure(yscrollcommand=appointments_scrollbar_y.set, xscrollcommand=appointments_scrollbar_x.set)

        appointments_scrollbar_y.pack(side="right", fill="y")
        appointments_scrollbar_x.pack(side="bottom", fill="x")
        self.appointments_tree.pack(fill="both", expand=True)

        actions_frame = ttk.Frame(daily_frame)
        actions_frame.pack(pady=10)
        ttk.Button(actions_frame, text="Marcar como Completada", command=lambda: self.update_appointment_status_ui('Completada')).pack(side="left", padx=5)
        ttk.Button(actions_frame, text="Procesar Cobro y Generar Recibo", command=self.process_payment_and_receipt).pack(side="left", padx=5)
        ttk.Button(actions_frame, text="Marcar como Cancelada", command=lambda: self.update_appointment_status_ui('Cancelada')).pack(side="left", padx=5)

        self.load_daily_appointments()

    def load_daily_appointments(self):
        for i in self.appointments_tree.get_children():
            self.appointments_tree.delete(i)

        date_to_load = self.daily_date_entry.get()
        appointments = appointment_scheduler.get_appointments_for_date(date_to_load)

        for appt in appointments:
            full_name = f"{appt[1]} {appt[2]}"
            self.appointments_tree.insert("", "end", values=(appt[0], full_name, appt[3], appt[4], f"${appt[5]:.2f}", appt[6]))

    def update_appointment_status_ui(self, new_status):
        selected_item = self.appointments_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una cita para actualizar su estado.")
            return

        appointment_id = self.appointments_tree.item(selected_item)['values'][0]
        appointment_scheduler.update_appointment_status(appointment_id, new_status)
        messagebox.showinfo("Actualización", f"Estado de la cita {appointment_id} actualizado a '{new_status}'.")
        self.load_daily_appointments()

    def process_payment_and_receipt(self):
        selected_item = self.appointments_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una cita para procesar el pago.")
            return

        appointment_data = self.appointments_tree.item(selected_item)['values']
        appointment_id = appointment_data[0]
        current_status = appointment_data[0]

        if current_status == 'Completada':
            if messagebox.askyesno("Recibo existente", "Esta cita ya ha sido marcada como completada. ¿Desea generar el recibo nuevamente?"):
                # Buscar factura existente para esta cita
                conn = database.connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM Facturas WHERE cita_id = ? ORDER BY id DESC LIMIT 1", (appointment_id,))
                existing_invoice_id_result = cursor.fetchone()
                conn.close()

                if existing_invoice_id_result:
                    invoice_id = existing_invoice_id_result[0]
                    success_pdf, filename_pdf = receipt_generator.generate_receipt_pdf(invoice_id)
                    if success_pdf:
                        messagebox.showinfo("Recibo Generado", f"El recibo ha sido generado como '{filename_pdf}'.")
                    else:
                        messagebox.showerror("Error de Recibo", f"Hubo un problema al generar el recibo PDF: {filename_pdf}")
                else:
                    messagebox.showerror("Error", "No se encontró una factura previa para esta cita.")
            return

        elif current_status == 'Cancelada':
            messagebox.showerror("Error", "No se puede procesar el pago para una cita cancelada.")
            return

        method = "Efectivo" 

        # Procesa el pago y obtiene el ID de la factura
        success_payment, message_payment, invoice_id = billing_system.process_payment(appointment_id, method)

        if success_payment:
            messagebox.showinfo("Pago Procesado", message_payment)
            self.load_daily_appointments() # Recargar para ver el estado actualizado

            if invoice_id:
                success_pdf, filename_pdf = receipt_generator.generate_receipt_pdf(invoice_id)
                if success_pdf:
                    messagebox.showinfo("Recibo Generado", f"El recibo ha sido guardado en '{filename_pdf}'.")
                else:
                    messagebox.showerror("Error de Recibo", f"Hubo un problema al generar el recibo PDF: {filename_pdf}")
            else:
                messagebox.showerror("Error", "No se pudo obtener el ID de la factura para generar el recibo.")

        else:
            messagebox.showerror("Error de Pago", message_payment)


if __name__ == "__main__":
    root = tk.Tk()
    app = BarberShopApp(root)
    root.mainloop()