# barberia_app/models/modelo_servicio.py
from core.modelo_db import ModelDB

class ModeloServicio:
    """
    Gestiona las operaciones de base de datos para los servicios.
    """
    def __init__(self, db_config):
        self.db = ModelDB(**db_config)

    def obtener_servicios(self):
        """
        Obtiene todos los servicios de la base de datos.
        """
        query = "SELECT * FROM servicios ORDER BY nombre_servicio"
        return self.db.ejecutar_consulta(query)

    def agregar_servicio(self, nombre_servicio, precio, duracion_estimada):
        """
        Agrega un nuevo servicio a la base de datos.
        """
        query = "INSERT INTO servicios (nombre_servicio, precio, duracion_estimada) VALUES (%s, %s, %s)"
        return self.db.ejecutar_consulta(query, (nombre_servicio, precio, duracion_estimada))

    def actualizar_servicio(self, id_servicio, nombre_servicio, precio, duracion_estimada):
        """
        Actualiza un servicio existente por su ID.
        """
        query = "UPDATE servicios SET nombre_servicio = %s, precio = %s, duracion_estimada = %s WHERE id_servicio = %s"
        return self.db.ejecutar_consulta(query, (nombre_servicio, precio, duracion_estimada, id_servicio))

    def eliminar_servicio(self, id_servicio):
        """
        Elimina un servicio de la base de datos por su ID.
        """
        query = "DELETE FROM servicios WHERE id_servicio = %s"
        return self.db.ejecutar_consulta(query, (id_servicio,))