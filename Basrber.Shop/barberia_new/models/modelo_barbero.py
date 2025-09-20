# barberia_app/models/modelo_barbero.py
from core.modelo_db import ModelDB

class ModeloBarbero:
    """
    Gestiona las operaciones de base de datos para los barberos.
    """
    def __init__(self, db_config):
        self.db = ModelDB(**db_config)

    def obtener_barberos(self):
        """
        Obtiene todos los barberos de la base de datos.
        """
        query = "SELECT * FROM barberos ORDER BY nombre, apellido"
        return self.db.ejecutar_consulta(query)

    def agregar_barbero(self, nombre, apellido, telefono):
        """
        Agrega un nuevo barbero a la base de datos.
        """
        query = "INSERT INTO barberos (nombre, apellido, telefono) VALUES (%s, %s, %s)"
        return self.db.ejecutar_consulta(query, (nombre, apellido, telefono))

    def actualizar_barbero(self, id_barbero, nombre, apellido, telefono):
        """
        Actualiza un barbero existente por su ID.
        """
        query = "UPDATE barberos SET nombre = %s, apellido = %s, telefono = %s WHERE id_barbero = %s"
        return self.db.ejecutar_consulta(query, (nombre, apellido, telefono, id_barbero))

    def eliminar_barbero(self, id_barbero):
        """
        Elimina un barbero de la base de datos por su ID.
        """
        query = "DELETE FROM barberos WHERE id_barbero = %s"
        return self.db.ejecutar_consulta(query, (id_barbero,))