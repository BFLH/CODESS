# barberia_app/controllers/controlador.py
from models.modelo_usuario import ModeloUsuario
from models.modelo_cliente import ModeloCliente
from models.modelo_barbero import ModeloBarbero
from models.modelo_servicio import ModeloServicio
from models.modelo_cita import ModeloCita

class Controlador:
    """
    Clase principal del Controlador que maneja la lógica de la aplicación,
    interactuando con los Modelos y coordinando con las Vistas.
    """
    def __init__(self, db_config):
        # Inicializamos los modelos, pasándoles la configuración de la base de datos
        self.modelo_usuario = ModeloUsuario(db_config)
        self.modelo_cliente = ModeloCliente(db_config)
        self.modelo_barbero = ModeloBarbero(db_config)
        self.modelo_servicio = ModeloServicio(db_config)
        self.modelo_cita = ModeloCita(db_config)
        
        self.vista_actual = None # Para mantener una referencia a la vista activa
        self.usuario_actual_rol = None # Para almacenar el rol del usuario logueado

    # --- Métodos de Autenticación ---
    def autenticar_usuario(self, nombre_usuario, contrasena):
        """
        Intenta autenticar al usuario. Si es exitoso, almacena el rol.
        """
        rol = self.modelo_usuario.autenticar_usuario(nombre_usuario, contrasena)
        if rol:
            self.usuario_actual_rol = rol
            print(f"Usuario {nombre_usuario} autenticado como {rol}.")
            return True
        print("Autenticación fallida.")
        return False

    def obtener_rol_usuario_actual(self):
        """
        Retorna el rol del usuario que ha iniciado sesión.
        """
        return self.usuario_actual_rol

    # --- Métodos de Gestión de Clientes ---
    def obtener_clientes(self):
        """
        Obtiene la lista de todos los clientes.
        """
        return self.modelo_cliente.obtener_clientes()

    def agregar_cliente(self, nombre, apellido, telefono, email):
        """
        Agrega un nuevo cliente.
        """
        return self.modelo_cliente.agregar_cliente(nombre, apellido, telefono, email)

    def actualizar_cliente(self, id_cliente, nombre, apellido, telefono, email):
        """
        Actualiza un cliente existente.
        """
        return self.modelo_cliente.actualizar_cliente(id_cliente, nombre, apellido, telefono, email)

    def eliminar_cliente(self, id_cliente):
        """
        Elimina un cliente por su ID.
        """
        return self.modelo_cliente.eliminar_cliente(id_cliente)

    # --- Métodos de Gestión de Barberos ---
    def obtener_barberos(self):
        """
        Obtiene la lista de todos los barberos.
        """
        return self.modelo_barbero.obtener_barberos()
    
    def agregar_barbero(self, nombre, apellido, telefono):
        """
        Agrega un nuevo barbero.
        """
        return self.modelo_barbero.agregar_barbero(nombre, apellido, telefono)

    def actualizar_barbero(self, id_barbero, nombre, apellido, telefono):
        """
        Actualiza un barbero existente.
        """
        return self.modelo_barbero.actualizar_barbero(id_barbero, nombre, apellido, telefono)

    def eliminar_barbero(self, id_barbero):
        """
        Elimina un barbero por su ID.
        """
        return self.modelo_barbero.eliminar_barbero(id_barbero)

    # --- Métodos de Gestión de Servicios ---
    def obtener_servicios(self):
        """
        Obtiene la lista de todos los servicios.
        """
        return self.modelo_servicio.obtener_servicios()

    def agregar_servicio(self, nombre_servicio, precio, duracion_estimada):
        """
        Agrega un nuevo servicio.
        """
        return self.modelo_servicio.agregar_servicio(nombre_servicio, precio, duracion_estimada)

    def actualizar_servicio(self, id_servicio, nombre_servicio, precio, duracion_estimada):
        """
        Actualiza un servicio existente.
        """
        return self.modelo_servicio.actualizar_servicio(id_servicio, nombre_servicio, precio, duracion_estimada)

    def eliminar_servicio(self, id_servicio):
        """
        Elimina un servicio por su ID.
        """
        return self.modelo_servicio.eliminar_servicio(id_servicio)

    # --- Métodos de Gestión de Citas ---
    def obtener_citas(self):
        """
        Obtiene la lista de todas las citas.
        """
        return self.modelo_cita.obtener_citas()

    def obtener_citas_en_espera(self):
        """
        Obtiene la lista de citas con estado 'En Espera'.
        """
        return self.modelo_cita.obtener_citas_en_espera()

    def agregar_cita(self, id_cliente, id_barbero, id_servicio, fecha_cita, hora_cita, estado='Programada'):
        """
        Agrega una nueva cita.
        """
        return self.modelo_cita.agregar_cita(id_cliente, id_barbero, id_servicio, fecha_cita, hora_cita, estado)

    def actualizar_cita(self, id_cita, id_cliente, id_barbero, id_servicio, fecha_cita, hora_cita, estado):
        """
        Actualiza una cita existente.
        """
        return self.modelo_cita.actualizar_cita(id_cita, id_cliente, id_barbero, id_servicio, fecha_cita, hora_cita, estado)

    def eliminar_cita(self, id_cita):
        """
        Elimina una cita por su ID.
        """
        return self.modelo_cita.eliminar_cita(id_cita)

    def cambiar_estado_cita(self, id_cita, nuevo_estado):
        """
        Cambia el estado de una cita.
        """
        return self.modelo_cita.cambiar_estado_cita(id_cita, nuevo_estado)