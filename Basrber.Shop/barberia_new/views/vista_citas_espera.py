# barberia_app/views/vista_citas_espera.py
import tkinter as tk
from tkinter import ttk, messagebox
from .base_vista import BaseVista
import datetime

class VistaCitasEspera(BaseVista):
    """
    Panel para mostrar las citas en estado 'En Espera'.
    Permite cambiar el estado de la cita.
    """
    def __init__(self, parent, controlador):
        super().__init__(parent, controlador)
        self.create_widgets()
        self.actualizar_citas_espera() # Cargar las citas al iniciar el panel

    def create_widgets(self):
        """
        Crea los widgets del panel de citas en espera.
        """
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill='both')

        title_label = ttk.Label(main_frame, text="Clientes en Espera", font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)

        # --- Tabla de Citas en Espera (Treeview) ---
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        self.espera_tree = ttk.Treeview(tree_frame, columns=("ID", "Cliente", "Barbero", "Servicio", "Fecha", "Hora"),
                                       show="headings",
                                       yscrollcommand=scrollbar_y.set,
                                       xscrollcommand=scrollbar_x.set)
        self.espera_tree.pack(expand=True, fill='both')

        scrollbar_y.config(command=self.espera_tree.yview)
        scrollbar_x.config(command=self.espera_tree.xview)

        # Definir encabezados de columna
        self.espera_tree.heading("ID", text="ID")
        self.espera_tree.heading("Cliente", text="Cliente")
        self.espera_tree.heading("Barbero", text="Barbero")
        self.espera_tree.heading("Servicio", text="Servicio")
        self.espera_tree.heading("Fecha", text="Fecha")
        self.espera_tree.heading("Hora", text="Hora")

        # Ajustar ancho de columnas
        self.espera_tree.column("ID", width=50, stretch=tk.NO, anchor="center")
        self.espera_tree.column("Cliente", width=180, anchor="w")
        self.espera_tree.column("Barbero", width=120, anchor="w")
        self.espera_tree.column("Servicio", width=180, anchor="w")
        self.espera_tree.column("Fecha", width=100, anchor="center")
        self.espera_tree.column("Hora", width=80, anchor="center")

        # --- Botones de Acción para Citas en Espera ---
        button_frame = ttk.Frame(main_frame, padding="5")
        button_frame.pack(pady=10, fill='x', padx=10)

        self.btn_completar = ttk.Button(button_frame, text="Marcar como Completada", command=self.marcar_completada, state=tk.DISABLED)
        self.btn_completar.pack(side=tk.LEFT, padx=5)

        self.btn_mover_programada = ttk.Button(button_frame, text="Mover a Programada", command=self.marcar_programada, state=tk.DISABLED)
        self.btn_mover_programada.pack(side=tk.LEFT, padx=5)

        self.btn_cancelar_espera = ttk.Button(button_frame, text="Cancelar Cita", command=self.cancelar_cita_espera, state=tk.DISABLED)
        self.btn_cancelar_espera.pack(side=tk.LEFT, padx=5)

        # Asociar evento de selección a la tabla
        self.espera_tree.bind("<<TreeviewSelect>>", self.seleccionar_cita_espera)


    def actualizar_citas_espera(self):
        """
        Obtiene las citas 'En Espera' del controlador y las muestra en la tabla.
        """
        for item in self.espera_tree.get_children():
            self.espera_tree.delete(item)

        citas_espera = self.controlador.obtener_citas_en_espera()
        if citas_espera:
            for cita in citas_espera:
                self.espera_tree.insert("", tk.END, values=(
                    cita['id_cita'],
                    f"{cita['cliente_nombre']} {cita['cliente_apellido']}",
                    f"{cita['barbero_nombre']} {cita['barbero_apellido']}",
                    cita['nombre_servicio'],
                    cita['fecha_cita'],
                    cita['hora_cita']
                ), iid=cita['id_cita']) # Usamos el id_cita como iid para facilitar la selección
        self.deshabilitar_botones_espera()

    def seleccionar_cita_espera(self, event):
        """
        Habilita los botones de acción cuando se selecciona una cita en espera.
        """
        selected_item_id = self.espera_tree.focus()
        if selected_item_id:
            self.cita_espera_seleccionada_id = selected_item_id
            self.btn_completar.config(state=tk.NORMAL)
            self.btn_mover_programada.config(state=tk.NORMAL)
            self.btn_cancelar_espera.config(state=tk.NORMAL)
        else:
            self.deshabilitar_botones_espera()

    def deshabilitar_botones_espera(self):
        """Deshabilita los botones de acción de citas en espera."""
        self.btn_completar.config(state=tk.DISABLED)
        self.btn_mover_programada.config(state=tk.DISABLED)
        self.btn_cancelar_espera.config(state=tk.DISABLED)
        if hasattr(self, 'cita_espera_seleccionada_id'):
            delattr(self, 'cita_espera_seleccionada_id')

    def marcar_completada(self):
        """
        Cambia el estado de la cita seleccionada a 'Completada'.
        """
        if not hasattr(self, 'cita_espera_seleccionada_id'):
            messagebox.showerror("Error", "Debe seleccionar una cita para marcar como completada.")
            return

        if messagebox.askyesno("Confirmar", "¿Marcar esta cita como completada?"):
            if self.controlador.cambiar_estado_cita(self.cita_espera_seleccionada_id, 'Completada'):
                messagebox.showinfo("Éxito", "Cita marcada como completada.")
                self.actualizar_citas_espera()
                # Opcional: refrescar también la vista de citas general si está abierta
                # self.parent.panel_citas.actualizar_citas()
            else:
                messagebox.showerror("Error", "No se pudo marcar la cita como completada.")

    def marcar_programada(self):
        """
        Cambia el estado de la cita seleccionada a 'Programada'.
        """
        if not hasattr(self, 'cita_espera_seleccionada_id'):
            messagebox.showerror("Error", "Debe seleccionar una cita para mover a programada.")
            return

        if messagebox.askyesno("Confirmar", "¿Mover esta cita a estado 'Programada'?"):
            if self.controlador.cambiar_estado_cita(self.cita_espera_seleccionada_id, 'Programada'):
                messagebox.showinfo("Éxito", "Cita movida a programada.")
                self.actualizar_citas_espera()
            else:
                messagebox.showerror("Error", "No se pudo mover la cita a programada.")

    def cancelar_cita_espera(self):
        """
        Cambia el estado de la cita seleccionada a 'Cancelada'.
        """
        if not hasattr(self, 'cita_espera_seleccionada_id'):
            messagebox.showerror("Error", "Debe seleccionar una cita para cancelar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de cancelar esta cita?"):
            if self.controlador.cambiar_estado_cita(self.cita_espera_seleccionada_id, 'Cancelada'):
                messagebox.showinfo("Éxito", "Cita cancelada.")
                self.actualizar_citas_espera()
            else:
                messagebox.showerror("Error", "No se pudo cancelar la cita.")