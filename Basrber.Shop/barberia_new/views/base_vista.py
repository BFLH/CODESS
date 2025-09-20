# barberia_app/views/base_vista.py
import tkinter as tk
from tkinter import ttk

class BaseVista(ttk.Frame):
    """
    Clase base para todas las vistas de la aplicación.
    Proporciona una referencia al controlador.
    """
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador # El controlador se pasa a cada vista
        self.parent = parent