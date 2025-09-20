# barberia_app/main.py
import tkinter as tk
from controllers.controlador import Controlador
from views.vista_login import VistaLogin
from views.vista_principal import VistaPrincipal

class BarberiaApp:
    def __init__(self, root):
        self.root = root
        #self.root.withdraw() # Oculta la ventana principal (root) al inicio

        self.root.title("Barbería App") # Título de la ventana principal, aunque esté oculta
        self.root.geometry("1x1+0+0") # Tamaño mínimo para que Tkinter funcione correctamente
        self.root.resizable(False, False) # Intenta centrar la ventana root si fuera visible

        # --- Configuración de la Base de Datos ---
        
        self.db_config = {
            'host': 'localhost',
            'database': 'barberia_db',
            'user': 'root',
            'password': '123' 
        }

        # --- Instanciar el Controlador ---
        self.controlador = Controlador(self.db_config)

        # --- Mostrar la ventana de Login ---
        self.vista_login = VistaLogin(self.root, self.controlador)
        # Este método se llamará desde VistaLogin cuando el login sea exitoso
        self.root.after_login_success = self.show_main_app 

    def show_main_app(self):
        """
        Muestra la ventana principal de la aplicación después de un login exitoso.
        """
        self.vista_principal = VistaPrincipal(self.root, self.controlador)
        self.vista_principal.deiconify() # Muestra la ventana principal
        self.root.withdraw() # Asegura que la ventana root esté oculta
        print("Ventana principal mostrada.")

    def run(self):
        """
        Inicia el bucle principal de Tkinter.
        """
        self.root.mainloop()

if __name__ == "__main__":
    # Crear la ventana raíz de Tkinter
    root = tk.Tk()
    
    # Crear e iniciar la aplicación
    app = BarberiaApp(root)
    app.run()