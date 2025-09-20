# barberia_app/views/vista_citas.py
import tkinter as tk
from tkinter import ttk, messagebox
from .base_vista import BaseVista
import datetime

class VistaCitas(BaseVista):
    """
    Panel para la gestión de citas (CRUD).
    """
    def __init__(self, parent, controlador):
        super().__init__(parent, controlador)
        self.clientes_disponibles = []
        self.barberos_disponibles = []
        self.servicios_disponibles = []
        self.create_widgets()
        self.cargar_comboboxes()
        self.actualizar_citas() # Cargar las citas al iniciar el panel

    def create_widgets(self):
        """
        Crea los widgets del panel de citas.
        """
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill='both')

        # --- Sección de Formulario (Entrada de Datos) ---
        form_frame = ttk.LabelFrame(main_frame, text="Programar Cita", padding="15")
        form_frame.pack(pady=10, padx=10, fill='x')

        # Cliente
        ttk.Label(form_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cliente_combobox = ttk.Combobox(form_frame, width=37, state="readonly")
        self.cliente_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Barbero
        ttk.Label(form_frame, text="Barbero:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.barbero_combobox = ttk.Combobox(form_frame, width=37, state="readonly")
        self.barbero_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Servicio
        ttk.Label(form_frame, text="Servicio:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.servicio_combobox = ttk.Combobox(form_frame, width=37, state="readonly")
        self.servicio_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Fecha
        ttk.Label(form_frame, text="Fecha (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.fecha_entry = ttk.Entry(form_frame, width=40)
        self.fecha_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.fecha_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d')) # Fecha actual por defecto

        # Hora
        ttk.Label(form_frame, text="Hora (HH:MM):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.hora_entry = ttk.Entry(form_frame, width=40)
        self.hora_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.hora_entry.insert(0, "09:00") # Hora por defecto

        # Estado (para modificar o cuando se agrega una cita directamente 'En Espera')
        ttk.Label(form_frame, text="Estado:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.estado_combobox = ttk.Combobox(form_frame, width=37, state="readonly",
                                            values=["Programada", "En Espera", "Completada", "Cancelada"])
        self.estado_combobox.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.estado_combobox.set("Programada") # Estado por defecto

        form_frame.grid_columnconfigure(1, weight=1)

        # --- Botones de Acción ---
        button_frame = ttk.Frame(main_frame, padding="5")
        button_frame.pack(pady=5, fill='x', padx=10)

        self.btn_agregar = ttk.Button(button_frame, text="Programar Cita", command=self.agregar_cita)
        self.btn_agregar.pack(side=tk.LEFT, padx=5)

        self.btn_modificar = ttk.Button(button_frame, text="Modificar Cita", command=self.modificar_cita, state=tk.DISABLED)
        self.btn_modificar.pack(side=tk.LEFT, padx=5)

        self.btn_eliminar = ttk.Button(button_frame, text="Eliminar Cita", command=self.eliminar_cita, state=tk.DISABLED)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        self.btn_limpiar = ttk.Button(button_frame, text="Limpiar", command=self.limpiar_campos)
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)

        # --- Tabla de Citas (Treeview) ---
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")


        self.citas_tree = ttk.Treeview(tree_frame, columns=("ID", "Cliente", "Barbero", "Servicio", "Fecha", "Hora", "Estado"),
                                       show="headings",
                                       yscrollcommand=scrollbar_y.set,
                                       xscrollcommand=scrollbar_x.set)
        self.citas_tree.pack(expand=True, fill='both')

        scrollbar_y.config(command=self.citas_tree.yview)
        scrollbar_x.config(command=self.citas_tree.xview)

        # Definir encabezados de columna
        self.citas_tree.heading("ID", text="ID")
        self.citas_tree.heading("Cliente", text="Cliente")
        self.citas_tree.heading("Barbero", text="Barbero")
        self.citas_tree.heading("Servicio", text="Servicio")
        self.citas_tree.heading("Fecha", text="Fecha")
        self.citas_tree.heading("Hora", text="Hora")
        self.citas_tree.heading("Estado", text="Estado")

        # Ajustar ancho de columnas
        self.citas_tree.column("ID", width=50, stretch=tk.NO, anchor="center")
        self.citas_tree.column("Cliente", width=150, anchor="w")
        self.citas_tree.column("Barbero", width=100, anchor="w")
        self.citas_tree.column("Servicio", width=150, anchor="w")
        self.citas_tree.column("Fecha", width=100, anchor="center")
        self.citas_tree.column("Hora", width=80, anchor="center")
        self.citas_tree.column("Estado", width=100, anchor="center")

        # Asociar evento de selección a la tabla
        self.citas_tree.bind("<<TreeviewSelect>>", self.seleccionar_cita)

    def cargar_comboboxes(self):
        """
        Carga los datos en los comboboxes de clientes, barberos y servicios.
        """
        self.clientes_disponibles = self.controlador.obtener_clientes()
        if self.clientes_disponibles:
            self.cliente_combobox['values'] = [f"{c['nombre']} {c['apellido']}" for c in self.clientes_disponibles]
            
        self.barberos_disponibles = self.controlador.obtener_barberos()
        if self.barberos_disponibles:
            self.barbero_combobox['values'] = [f"{b['nombre']} {b['apellido']}" for b in self.barberos_disponibles]

        self.servicios_disponibles = self.controlador.obtener_servicios()
        if self.servicios_disponibles:
            self.servicio_combobox['values'] = [s['nombre_servicio'] for s in self.servicios_disponibles]

    def limpiar_campos(self):
        """Limpia los campos del formulario de citas y restablece los botones."""
        self.cliente_combobox.set('')
        self.barbero_combobox.set('')
        self.servicio_combobox.set('')
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))
        self.hora_entry.delete(0, tk.END)
        self.hora_entry.insert(0, "09:00")
        self.estado_combobox.set("Programada")
        self.citas_tree.selection_remove(self.citas_tree.selection())

        self.btn_agregar.config(state=tk.NORMAL)
        self.btn_modificar.config(state=tk.DISABLED)
        self.btn_eliminar.config(state=tk.DISABLED)

    def actualizar_citas(self):
        """
        Obtiene las citas del controlador y las muestra en la tabla.
        """
        for item in self.citas_tree.get_children():
            self.citas_tree.delete(item)

        citas = self.controlador.obtener_citas()
        if citas:
            for cita in citas:
                # El modelo de cita ya trae los nombres, no solo IDs
                self.citas_tree.insert("", tk.END, values=(
                    cita['id_cita'],
                    f"{cita['cliente_nombre']} {cita['cliente_apellido']}",
                    f"{cita['barbero_nombre']} {cita['barbero_apellido']}",
                    cita['nombre_servicio'],
                    cita['fecha_cita'],
                    cita['hora_cita'],
                    cita['estado']
                ), iid=cita['id_cita']) # Usamos el id_cita como iid para facilitar la selección

        self.limpiar_campos() # Asegurarse de que los campos estén limpios después de la actualización

    def agregar_cita(self):
        """
        Obtiene los datos del formulario y los envía al controlador para agregar una cita.
        """
        cliente_texto = self.cliente_combobox.get()
        barbero_texto = self.barbero_combobox.get()
        servicio_texto = self.servicio_combobox.get()
        fecha_str = self.fecha_entry.get().strip()
        hora_str = self.hora_entry.get().strip()
        estado = self.estado_combobox.get()

        # Validar selección de combobox
        if not cliente_texto or not barbero_texto or not servicio_texto:
            messagebox.showerror("Error de Datos", "Debe seleccionar un cliente, barbero y servicio.")
            return

        # Obtener los IDs reales
        id_cliente = next((c['id_cliente'] for c in self.clientes_disponibles if f"{c['nombre']} {c['apellido']}" == cliente_texto), None)
        id_barbero = next((b['id_barbero'] for b in self.barberos_disponibles if f"{b['nombre']} {b['apellido']}" == barbero_texto), None)
        id_servicio = next((s['id_servicio'] for s in self.servicios_disponibles if s['nombre_servicio'] == servicio_texto), None)

        if not all([id_cliente, id_barbero, id_servicio]):
            messagebox.showerror("Error Interno", "No se pudo encontrar el ID del cliente, barbero o servicio seleccionado.")
            return

        # Validar formato de fecha y hora
        try:
            fecha_cita = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora_cita = datetime.datetime.strptime(hora_str, '%H:%M').time()
        except ValueError:
            messagebox.showerror("Error de Formato", "Formato de fecha o hora inválido. Use YYYY-MM-DD y HH:MM.")
            return

        if self.controlador.agregar_cita(id_cliente, id_barbero, id_servicio, fecha_cita, hora_cita, estado):
            messagebox.showinfo("Éxito", "Cita programada correctamente.")
            self.actualizar_citas()
        else:
            messagebox.showerror("Error", "No se pudo programar la cita. Intente de nuevo.")

    def seleccionar_cita(self, event):
        """
        Carga los datos de la cita seleccionada en la tabla a los campos del formulario.
        """
        selected_item_id = self.citas_tree.focus()
        if selected_item_id:
            # Recuperar los valores del item seleccionado del Treeview
            values = self.citas_tree.item(selected_item_id, 'values')
            self.cita_seleccionada_id = values[0] # El ID de la cita

            # Limpiar campos antes de cargar
            self.limpiar_campos() 

            # Cargar los datos en los comboboxes y campos de texto
            self.cliente_combobox.set(values[1]) # "Nombre Apellido Cliente"
            self.barbero_combobox.set(values[2]) # "Nombre Apellido Barbero"
            self.servicio_combobox.set(values[3]) # "Nombre Servicio"
            self.fecha_entry.insert(0, str(values[4])) # Fecha
            self.hora_entry.insert(0, str(values[5])) # Hora
            self.estado_combobox.set(values[6]) # Estado

            # Habilitar botones de modificar y eliminar
            self.btn_agregar.config(state=tk.DISABLED)
            self.btn_modificar.config(state=tk.NORMAL)
            self.btn_eliminar.config(state=tk.NORMAL)
        else:
            self.limpiar_campos()


    def modificar_cita(self):
        """
        Obtiene los datos del formulario y los envía al controlador para modificar una cita.
        """
        if not hasattr(self, 'cita_seleccionada_id'):
            messagebox.showerror("Error", "Debe seleccionar una cita para modificar.")
            return

        cliente_texto = self.cliente_combobox.get()
        barbero_texto = self.barbero_combobox.get()
        servicio_texto = self.servicio_combobox.get()
        fecha_str = self.fecha_entry.get().strip()
        hora_str = self.hora_entry.get().strip()
        estado = self.estado_combobox.get()

        if not cliente_texto or not barbero_texto or not servicio_texto:
            messagebox.showerror("Error de Datos", "Debe seleccionar un cliente, barbero y servicio.")
            return

        id_cliente = next((c['id_cliente'] for c in self.clientes_disponibles if f"{c['nombre']} {c['apellido']}" == cliente_texto), None)
        id_barbero = next((b['id_barbero'] for b in self.barberos_disponibles if f"{b['nombre']} {b['apellido']}" == barbero_texto), None)
        id_servicio = next((s['id_servicio'] for s in self.servicios_disponibles if s['nombre_servicio'] == servicio_texto), None)

        if not all([id_cliente, id_barbero, id_servicio]):
            messagebox.showerror("Error Interno", "No se pudo encontrar el ID del cliente, barbero o servicio seleccionado.")
            return
        
        try:
            fecha_cita = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora_cita = datetime.datetime.strptime(hora_str, '%H:%M').time()
        except ValueError:
            messagebox.showerror("Error de Formato", "Formato de fecha o hora inválido. Use YYYY-MM-DD y HH:MM.")
            return

        if messagebox.askyesno("Confirmar Modificación", "¿Está seguro de modificar esta cita?"):
            if self.controlador.actualizar_cita(self.cita_seleccionada_id, id_cliente, id_barbero, id_servicio, fecha_cita, hora_cita, estado):
                messagebox.showinfo("Éxito", "Cita modificada correctamente.")
                self.actualizar_citas()
            else:
                messagebox.showerror("Error", "No se pudo modificar la cita. Intente de nuevo.")

    def eliminar_cita(self):
        """
        Envía la solicitud al controlador para eliminar una cita.
        """
        if not hasattr(self, 'cita_seleccionada_id'):
            messagebox.showerror("Error", "Debe seleccionar una cita para eliminar.")
            return

        if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de eliminar esta cita?"):
            if self.controlador.eliminar_cita(self.cita_seleccionada_id):
                messagebox.showinfo("Éxito", "Cita eliminada correctamente.")
                delattr(self, 'cita_seleccionada_id')
                self.actualizar_citas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la cita. Intente de nuevo.")