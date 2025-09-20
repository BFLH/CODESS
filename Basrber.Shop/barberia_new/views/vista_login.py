# barberia_app/views/vista_login.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
# Importar Pillow
from PIL import Image, ImageTk # <-- Añade esta línea

class VistaLogin(tk.Toplevel):
    """
    Ventana de inicio de sesión para la aplicación.
    """
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.parent = parent
        self.controlador = controlador

        self.title("Iniciar Sesión - Barbería")
        # Ajustamos el tamaño para acomodar la imagen redimensionada
        # Ajusta estas dimensiones según cómo quieras que se vea el logo y el formulario
        self.geometry("700x400") # ANTES: 650x380. Un poco más grande para el logo.
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Lógica para centrar la ventana
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"+{x}+{y}")

        # Cargar la imagen del logo usando Pillow
        self.logo_image_tk = None # Usaremos este para Tkinter
        
        base_dir_for_assets = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets'))
        logo_path = os.path.join(base_dir_for_assets, 'logo_barberia.jpg') # <-- Asegúrate que sea .jpg
        
        # Dimensiones deseadas para el logo dentro de la ventana
        # Puedes ajustar estos valores según cómo quieras que se vea
        desired_width = 300 
        desired_height = 300 # El logo es cuadrado, así que mantenemos proporciones

        try:
            # 1. Cargar la imagen con PIL
            original_image = Image.open(logo_path)
            
            # 2. Redimensionar la imagen manteniendo la proporción
            # Calcula las nuevas dimensiones para encajar manteniendo el aspect ratio
            original_width, original_height = original_image.size
            if original_width > desired_width or original_height > desired_height:
                ratio = min(desired_width / original_width, desired_height / original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
            else:
                resized_image = original_image # Si ya es pequeña o del tamaño deseado, no la redimensiones

            # 3. Convertir la imagen de PIL a un formato que Tkinter pueda usar
            self.logo_image_tk = ImageTk.PhotoImage(resized_image)
            print(f"Logo cargado y redimensionado a {new_width}x{new_height}.")

        except FileNotFoundError:
            print(f"Advertencia: El archivo del logo no se encontró en: {logo_path}")
        except Exception as e: # Captura otros errores (como si no es un formato válido)
            print(f"Advertencia: No se pudo cargar o procesar el logo desde '{logo_path}': {e}")

        self.create_widgets()

        self.transient(parent)
        self.grab_set()

    def create_widgets(self):
        """
        Crea los widgets de la interfaz de login.
        """
        style = ttk.Style()
        style.configure('TFrame', background='#F0F0F0')
        style.configure('TLabel', background='#F0F0F0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'))

        # --- Frame principal que usará GRID ---
        # Aumentamos el padding para dar más respiro
        main_frame = ttk.Frame(self, padding="20 30 20 30") # top y bottom padding
        main_frame.pack(expand=True, fill='both')

        # Configurar las columnas para el grid de main_frame
        main_frame.columnconfigure(0, weight=1) # Columna para el formulario de login (izquierda)
        main_frame.columnconfigure(1, weight=1) # Columna para la imagen (derecha)
        main_frame.rowconfigure(0, weight=1) # Una sola fila

        # --- Contenedor para el Formulario de Login (columna izquierda) ---
        login_form_frame = ttk.Frame(main_frame, padding="10")
        login_form_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Título
        title_label = ttk.Label(login_form_frame, text="Acceso a la Barbería", font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)

        # Usuario
        ttk.Label(login_form_frame, text="Usuario:").pack(pady=(10, 0))
        self.usuario_entry = ttk.Entry(login_form_frame, width=30)
        self.usuario_entry.pack(pady=5)
        self.usuario_entry.focus_set()

        # Contraseña
        ttk.Label(login_form_frame, text="Contraseña:").pack(pady=(10, 0))
        self.contrasena_entry = ttk.Entry(login_form_frame, show="*", width=30)
        self.contrasena_entry.pack(pady=5)
        self.contrasena_entry.bind("<Return>", lambda event: self.handle_login())

        # Botón de Login
        login_button = ttk.Button(login_form_frame, text="Ingresar", command=self.handle_login)
        login_button.pack(pady=20)

        # --- Botón para cambiar contraseña ---
        cambiar_contra_button = ttk.Button(
            login_form_frame, 
            text="Cambiar contraseña", 
            command=self.abrir_cambiar_contrasena
        )
        cambiar_contra_button.pack(pady=(0, 10))

        # --- Contenedor para la Imagen (columna derecha) ---
        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        if self.logo_image_tk: # <-- Usamos self.logo_image_tk ahora
            logo_label = ttk.Label(image_frame, image=self.logo_image_tk, background='#F0F0F0')
            logo_label.pack(expand=True, fill='both')
        else:
            ttk.Label(image_frame, text="[Logo no cargado]", background='#F0F0F0').pack(expand=True)

    def handle_login(self):
        """
        Maneja la lógica del botón de login.
        Recoge los datos y los envía al controlador para autenticar.
        """
        nombre_usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        if self.controlador.autenticar_usuario(nombre_usuario, contrasena):
            messagebox.showinfo("Login Exitoso", f"Bienvenido, {nombre_usuario}!")
            self.destroy() # Cierra la ventana de login
            self.parent.after_login_success() # Notifica a la ventana principal
        else:
            messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")
            self.contrasena_entry.delete(0, tk.END) # Limpiar campo de contraseña

    def on_closing(self):
        """
        Maneja el evento de cierre de la ventana (cruz).
        Si se cierra la ventana de login, cierra la aplicación principal.
        """
        if messagebox.askokcancel("Salir", "¿Deseas salir de la aplicación?"):
            self.parent.destroy() # Cierra la ventana principal

    def abrir_cambiar_contrasena(self):
        ventana = tk.Toplevel(self)
        ventana.title("Cambiar contraseña")
        ventana.geometry("400x300")  # Más amplia
        ventana.resizable(False, False)
        ventana.transient(self)
        ventana.grab_set()

        ttk.Label(ventana, text="Usuario:").pack(pady=(25, 0))
        usuario_entry = ttk.Entry(ventana, width=35)
        usuario_entry.pack(pady=5)

        ttk.Label(ventana, text="Nueva contraseña:").pack(pady=(15, 0))
        nueva_entry = ttk.Entry(ventana, show="*", width=35)
        nueva_entry.pack(pady=5)

        ttk.Label(ventana, text="Confirmar contraseña:").pack(pady=(15, 0))
        confirmar_entry = ttk.Entry(ventana, show="*", width=35)
        confirmar_entry.pack(pady=5)

        def cambiar():
            usuario = usuario_entry.get().strip()
            nueva = nueva_entry.get().strip()
            confirmar = confirmar_entry.get().strip()
            if not usuario or not nueva or not confirmar:
                messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=ventana)
                return
            if nueva != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden.", parent=ventana)
                return
            # Verificar si el usuario existe antes de cambiar la contraseña
            usuario_db = self.controlador.modelo_usuario.db.ejecutar_consulta(
                "SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s", (usuario,)
            )
            if not usuario_db:
                messagebox.showerror("Error", "El usuario no existe.", parent=ventana)
                usuario_entry.delete(0, tk.END)
                nueva_entry.delete(0, tk.END)
                confirmar_entry.delete(0, tk.END)
                return
            # Cambiar la contraseña
            if self.controlador.modelo_usuario.actualizar_usuario_por_nombre(usuario, nueva):
                messagebox.showinfo("Éxito", "Contraseña cambiada correctamente.", parent=ventana)
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo cambiar la contraseña. Intente de nuevo.", parent=ventana)

        ttk.Button(ventana, text="Cambiar", command=cambiar).pack(pady=25)