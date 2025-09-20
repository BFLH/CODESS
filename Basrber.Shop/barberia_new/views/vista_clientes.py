# barberia_app/views/vista_clientes.py
import tkinter as tk
from tkinter import ttk, messagebox
from .base_vista import BaseVista

class VistaClientes(BaseVista):
    """
    Panel para la gestión de clientes (CRUD).
    """
    def __init__(self, parent, controlador):
        super().__init__(parent, controlador)
        self.create_widgets()
        self.actualizar_clientes() # Cargar los clientes al iniciar el panel

    def create_widgets(self):
        """
        Crea los widgets del panel de clientes.
        """
        # Frame principal para el formulario y la tabla
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill='both')

        # --- Sección de Formulario (Entrada de Datos) ---
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Cliente", padding="15")
        form_frame.pack(pady=10, padx=10, fill='x')

        # Labels y Entries para los campos del cliente
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nombre_entry = ttk.Entry(form_frame, width=40)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Apellido:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.apellido_entry = ttk.Entry(form_frame, width=40)
        self.apellido_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.telefono_entry = ttk.Entry(form_frame, width=40)
        self.telefono_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = ttk.Entry(form_frame, width=40)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Configurar la expansión de columnas para el formulario
        form_frame.grid_columnconfigure(1, weight=1)

        # --- Botones de Acción ---
        button_frame = ttk.Frame(main_frame, padding="5")
        button_frame.pack(pady=5, fill='x', padx=10)

        self.btn_agregar = ttk.Button(button_frame, text="Agregar", command=self.agregar_cliente)
        self.btn_agregar.pack(side=tk.LEFT, padx=5)

        self.btn_modificar = ttk.Button(button_frame, text="Modificar", command=self.modificar_cliente, state=tk.DISABLED)
        self.btn_modificar.pack(side=tk.LEFT, padx=5)

        self.btn_eliminar = ttk.Button(button_frame, text="Eliminar", command=self.eliminar_cliente, state=tk.DISABLED)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        self.btn_limpiar = ttk.Button(button_frame, text="Limpiar", command=self.limpiar_campos)
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)

        # --- Tabla de Clientes (Treeview) ---
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.clientes_tree = ttk.Treeview(tree_frame, columns=("ID", "Nombre", "Apellido", "Teléfono", "Email"), show="headings", yscrollcommand=scrollbar.set)
        self.clientes_tree.pack(expand=True, fill='both')

        scrollbar.config(command=self.clientes_tree.yview)

        # Definir encabezados de columna
        self.clientes_tree.heading("ID", text="ID")
        self.clientes_tree.heading("Nombre", text="Nombre")
        self.clientes_tree.heading("Apellido", text="Apellido")
        self.clientes_tree.heading("Teléfono", text="Teléfono")
        self.clientes_tree.heading("Email", text="Email")

        # Ajustar ancho de columnas (opcional)
        self.clientes_tree.column("ID", width=50, stretch=tk.NO, anchor="center")
        self.clientes_tree.column("Nombre", width=150, anchor="w")
        self.clientes_tree.column("Apellido", width=150, anchor="w")
        self.clientes_tree.column("Teléfono", width=100, anchor="center")
        self.clientes_tree.column("Email", width=200, anchor="w")

        # Asociar evento de selección a la tabla
        self.clientes_tree.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

    def limpiar_campos(self):
        """Limpia los campos del formulario y restablece los botones."""
        self.nombre_entry.delete(0, tk.END)
        self.apellido_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.clientes_tree.selection_remove(self.clientes_tree.selection()) # Deseleccionar item en el treeview

        self.btn_agregar.config(state=tk.NORMAL)
        self.btn_modificar.config(state=tk.DISABLED)
        self.btn_eliminar.config(state=tk.DISABLED)

    def actualizar_clientes(self):
        """
        Obtiene los clientes del controlador y los muestra en la tabla.
        """
        # Limpiar la tabla antes de insertar nuevos datos
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)

        clientes = self.controlador.obtener_clientes()
        if clientes:
            for cliente in clientes:
                self.clientes_tree.insert("", tk.END, values=(
                    cliente['id_cliente'],
                    cliente['nombre'],
                    cliente['apellido'],
                    cliente['telefono'],
                    cliente['email']
                ))
        self.limpiar_campos() # Asegurarse de que los campos estén limpios después de la actualización

    def agregar_cliente(self):
        """
        Obtiene los datos del formulario y los envía al controlador para agregar un cliente.
        """
        nombre = self.nombre_entry.get().strip()
        apellido = self.apellido_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validación: nombre y apellido solo letras, teléfono solo números
        if not nombre or not apellido:
            messagebox.showerror("Error de Datos", "Los campos Nombre y Apellido son obligatorios.")
            return
        if not nombre.isalpha():
            messagebox.showerror("Error de Datos", "El campo Nombre solo debe contener letras.")
            return
        if not apellido.isalpha():
            messagebox.showerror("Error de Datos", "El campo Apellido solo debe contener letras.")
            return
        if telefono and not telefono.isdigit():
            messagebox.showerror("Error de Datos", "El campo Teléfono solo debe contener números.")
            return

        if self.controlador.agregar_cliente(nombre, apellido, telefono, email):
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
            self.actualizar_clientes()
        else:
            messagebox.showerror("Error", "No se pudo agregar el cliente. Intente de nuevo.")

    def seleccionar_cliente(self, event):
        """
        Carga los datos del cliente seleccionado en la tabla a los campos del formulario.
        """
        selected_item = self.clientes_tree.focus() # Obtiene el ID del elemento seleccionado
        if selected_item:
            values = self.clientes_tree.item(selected_item, 'values')
            self.cliente_seleccionado_id = values[0] # Guardar el ID para modificar/eliminar

            self.limpiar_campos() # Limpiar antes de cargar nuevos datos
            self.nombre_entry.insert(0, values[1])
            self.apellido_entry.insert(0, values[2])
            self.telefono_entry.insert(0, values[3])
            self.email_entry.insert(0, values[4])

            # Habilitar botones de modificar y eliminar
            self.btn_agregar.config(state=tk.DISABLED)
            self.btn_modificar.config(state=tk.NORMAL)
            self.btn_eliminar.config(state=tk.NORMAL)
        else:
            self.limpiar_campos() # Si no hay selección, limpiar y deshabilitar

    def modificar_cliente(self):
        """
        Obtiene los datos del formulario y los envía al controlador para modificar un cliente.
        """
        if not hasattr(self, 'cliente_seleccionado_id'):
            messagebox.showerror("Error", "Debe seleccionar un cliente para modificar.")
            return

        nombre = self.nombre_entry.get().strip()
        apellido = self.apellido_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validación: nombre y apellido solo letras, teléfono solo números
        if not nombre or not apellido:
            messagebox.showerror("Error de Datos", "Los campos Nombre y Apellido son obligatorios.")
            return
        if not nombre.isalpha():
            messagebox.showerror("Error de Datos", "El campo Nombre solo debe contener letras.")
            return
        if not apellido.isalpha():
            messagebox.showerror("Error de Datos", "El campo Apellido solo debe contener letras.")
            return
        if telefono and not telefono.isdigit():
            messagebox.showerror("Error de Datos", "El campo Teléfono solo debe contener números.")
            return

        if messagebox.askyesno("Confirmar Modificación", "¿Está seguro de modificar este cliente?"):
            if self.controlador.actualizar_cliente(self.cliente_seleccionado_id, nombre, apellido, telefono, email):
                messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
                self.actualizar_clientes()
            else:
                messagebox.showerror("Error", "No se pudo modificar el cliente. Intente de nuevo.")

    def eliminar_cliente(self):
        """
        Envía la solicitud al controlador para eliminar un cliente.
        """
        if not hasattr(self, 'cliente_seleccionado_id'):
            messagebox.showerror("Error", "Debe seleccionar un cliente para eliminar.")
            return

        if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de eliminar este cliente?"):
            if self.controlador.eliminar_cliente(self.cliente_seleccionado_id):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                delattr(self, 'cliente_seleccionado_id') # Eliminar la referencia al ID
                self.actualizar_clientes()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente. Intente de nuevo.")