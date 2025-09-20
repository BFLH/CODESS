# barberia_app/models/modelo_cliente.py
from core.modelo_db import ModelDB

class ModeloCliente:
    """
    Gestiona las operaciones de base de datos para los clientes.
    """
    def __init__(self, db_config):
        self.db = ModelDB(**db_config)

    def obtener_clientes(self):
        """
        Obtiene todos los clientes de la base de datos.
        """
        query = "SELECT * FROM clientes ORDER BY nombre, apellido"
        return self.db.ejecutar_consulta(query)

    def agregar_cliente(self, nombre, apellido, telefono, email):
        """
        Agrega un nuevo cliente a la base de datos.
        """
        query = "INSERT INTO clientes (nombre, apellido, telefono, email) VALUES (%s, %s, %s, %s)"
        return self.db.ejecutar_consulta(query, (nombre, apellido, telefono, email))

    def actualizar_cliente(self, id_cliente, nombre, apellido, telefono, email):
        """
        Actualiza un cliente existente por su ID.
        """
        query = "UPDATE clientes SET nombre = %s, apellido = %s, telefono = %s, email = %s WHERE id_cliente = %s"
        return self.db.ejecutar_consulta(query, (nombre, apellido, telefono, email, id_cliente))

    def eliminar_cliente(self, id_cliente):
        """
        Elimina un cliente de la base de datos por su ID.
        """
        query = "DELETE FROM clientes WHERE id_cliente = %s"
        return self.db.ejecutar_consulta(query, (id_cliente,))