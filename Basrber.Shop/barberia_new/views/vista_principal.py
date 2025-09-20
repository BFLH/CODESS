# barberia_app/views/vista_principal.py
import tkinter as tk
from tkinter import ttk, messagebox
from .base_vista import BaseVista
# Importar las vistas de los paneles (aún no creadas, pero las importaremos aquí)
from .vista_clientes import VistaClientes
from .vista_citas import VistaCitas
from .vista_citas_espera import VistaCitasEspera
# Importar vista para gestión de usuarios/barberos/servicios si el rol es Admin
# from .vista_admin import VistaAdmin # La crearemos si se necesita un panel específico de admin
import os

class VistaPrincipal(tk.Toplevel):
    """
    Ventana principal de la aplicación, contiene las pestañas de navegación.
    """
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.parent = parent
        self.controlador = controlador
        self.usuario_rol = self.controlador.obtener_rol_usuario_actual()

        self.title("Gamma Barber")
        self.geometry("1000x700") # Un tamaño más generoso para la app principal
        self.state('zoomed') # Inicia la ventana maximizada
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.icons = {}  # Diccionario para almacenar las imágenes cargadas
        self.load_icons()  # Cargar los iconos al iniciar la ventana

        self.create_panels()

        # Ocultar la ventana principal hasta que el login sea exitoso
        self.withdraw()

    def load_icons(self):
        """
        Carga los iconos de la aplicación y los almacena.
        Asume que hay una carpeta 'assets' en la raíz del proyecto.
        """
        icon_names = {
            'cliente': 'cliente.png',
            'cita': 'cita.png',
            'espera': 'espera.png',
            # Puedes añadir más iconos aquí si los tienes
            # 'admin': 'admin.png',
            # 'barbero': 'barbero.png',
            # 'servicio': 'servicio.png',
        }
        
        # Obtener el directorio base de la aplicación (donde está main.py)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets_dir = os.path.join(base_dir, 'assets') # Carpeta assets al mismo nivel que barberia_app

        for name, filename in icon_names.items():
            icon_path = os.path.join(assets_dir, filename)
            try:
                # Intenta cargar la imagen. Si no existe o hay un error, se reporta.
                self.icons[name] = tk.PhotoImage(file=icon_path)
            except tk.TclError:
                print(f"Advertencia: No se pudo cargar el icono '{filename}' en {icon_path}.")
                self.icons[name] = None # Almacenar None si no se pudo cargar

    def get_icon(self, name):
        """
        Retorna la referencia al objeto PhotoImage para un icono dado.
        Retorna None si el icono no fue cargado.
        """
        return self.icons.get(name)

    def create_panels(self):
        """
        Crea los paneles (pestañas) de la aplicación según el rol del usuario.
        """
        # Panel de Clientes (disponible para ambos roles)
        self.panel_clientes = VistaClientes(self.notebook, self.controlador)
        # Condicionamos el uso de 'image' y 'compound'
        tab_options_cliente = {'text': "Clientes"}
        icon_cliente = self.get_icon('cliente')
        if icon_cliente:
            tab_options_cliente['image'] = icon_cliente
            tab_options_cliente['compound'] = tk.LEFT
        self.notebook.add(self.panel_clientes, **tab_options_cliente)

        # Panel de Citas (disponible para ambos roles)
        self.panel_citas = VistaCitas(self.notebook, self.controlador)
        tab_options_cita = {'text': "Citas"}
        icon_cita = self.get_icon('cita')
        if icon_cita:
            tab_options_cita['image'] = icon_cita
            tab_options_cita['compound'] = tk.LEFT
        self.notebook.add(self.panel_citas, **tab_options_cita)

        # Panel de Citas en Espera (disponible para ambos roles)
        self.panel_citas_espera = VistaCitasEspera(self.notebook, self.controlador)
        tab_options_espera = {'text': "En Espera"}
        icon_espera = self.get_icon('espera')
        if icon_espera:
            tab_options_espera['image'] = icon_espera
            tab_options_espera['compound'] = tk.LEFT
        self.notebook.add(self.panel_citas_espera, **tab_options_espera)

        # Paneles solo para Administrador
        if self.usuario_rol == 'Admin':
            # Puedes agregar pestañas adicionales aquí para administración de usuarios, barberos, servicios
            # Por ahora, podemos usar el panel de clientes para gestionar también usuarios si es simple
            # O crear un nuevo panel VistaAdmin si la lógica de administración es compleja.
            # Por ejemplo:
            # self.panel_admin = VistaAdmin(self.notebook, self.controlador)
            # self.notebook.add(self.panel_admin, text="Administración", image=self.get_icon('admin'), compound=tk.LEFT)
            pass # No agregamos un panel de admin específico por ahora para simplificar.

        # Refrescar los datos de las pestañas al cambiar entre ellas
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        """
        Método llamado cuando se cambia de pestaña.
        Permite refrescar los datos de la pestaña activa.
        """
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        print(f"Pestaña cambiada a: {selected_tab}")
        # Aquí puedes llamar a métodos de actualización específicos de cada panel
        if selected_tab == "Clientes":
            self.panel_clientes.actualizar_clientes()
        elif selected_tab == "Citas":
            self.panel_citas.actualizar_citas()
        elif selected_tab == "En Espera":
            self.panel_citas_espera.actualizar_citas_espera()

    def get_icon(self, name):
        """
        Carga y devuelve un icono.
        NOTA: Necesitarás tener archivos .png o .gif en una carpeta 'assets'
        o similar para que esto funcione. Por ahora, devolverá None si no los encuentra.
        """
        # Aquí deberías tener tus archivos de imagen.
        # Por ejemplo, en una carpeta 'assets' dentro de 'barberia_app'.
        # self.icons = {} # Diccionario para almacenar las imágenes cargadas
        # try:
        #     if name not in self.icons:
        #         path = f"assets/{name}.png" # Asegúrate de que esta ruta sea correcta
        #         self.icons[name] = tk.PhotoImage(file=path)
        #     return self.icons[name]
        # except tk.TclError:
        #     print(f"Advertencia: No se encontró el icono para '{name}'.")
        return None # Por ahora, devuelve None si no hay iconos

    def on_closing(self):
        """
        Maneja el cierre de la ventana principal.
        """
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres cerrar la aplicación?"):
            self.parent.destroy() # Cierra la ventana root