# barberia_app/models/modelo_cita.py
from core.modelo_db import ModelDB
from datetime import date, time

class ModeloCita:
    """
    Gestiona las operaciones de base de datos para las citas.
    """
    def __init__(self, db_config):
        self.db = ModelDB(**db_config)

    def obtener_citas(self):
        """
        Obtiene todas las citas, con información detallada de cliente, barbero y servicio.
        """
        query = """
        SELECT
            c.id_cita,
            cl.nombre AS cliente_nombre,
            cl.apellido AS cliente_apellido,
            b.nombre AS barbero_nombre,
            b.apellido AS barbero_apellido,
            s.nombre_servicio,
            c.fecha_cita,
            c.hora_cita,
            c.estado,
            c.id_cliente,
            c.id_barbero,
            c.id_servicio
        FROM citas c
        JOIN clientes cl ON c.id_cliente = cl.id_cliente
        JOIN barberos b ON c.id_barbero = b.id_barbero
        JOIN servicios s ON c.id_servicio = s.id_servicio
        ORDER BY c.fecha_cita, c.hora_cita;
        """
        return self.db.ejecutar_consulta(query)

    def obtener_citas_en_espera(self):
        """
        Obtiene las citas con estado 'En Espera'.
        """
        # Para una aplicación real, probablemente querrías filtrar por la fecha actual o futuras citas en espera
        query = """
        SELECT
            c.id_cita,
            cl.nombre AS cliente_nombre,
            cl.apellido AS cliente_apellido,
            b.nombre AS barbero_nombre,
            b.apellido AS barbero_apellido,
            s.nombre_servicio,
            c.fecha_cita,
            c.hora_cita,
            c.estado,
            c.id_cliente,
            c.id_barbero,
            c.id_servicio
        FROM citas c
        JOIN clientes cl ON c.id_cliente = cl.id_cliente
        JOIN barberos b ON c.id_barbero = b.id_barbero
        JOIN servicios s ON c.id_servicio = s.id_servicio
        WHERE c.estado = 'En Espera'
        ORDER BY c.fecha_cita, c.hora_cita;
        """
        return self.db.ejecutar_consulta(query)

    def agregar_cita(self, id_cliente, id_barbero, id_servicio, fecha_cita, hora_cita, estado='Programada'):
        """
        Agrega una nueva cita a la base de datos.
        """
        query = "INSERT INTO citas (id_cliente, id_barbero, id_servicio, fecha_cita, hora_cita, estado) VALUES (%s, %s, %s, %s, %s, %s)"
        return self.db.ejecutar_consulta(query, (id_cliente, id_barbero, id_servicio, fecha_cita, hora_cita, estado))

    def actualizar_cita(self, id_cita, id_cliente, id_barbero, id_servicio, fecha_cita, hora_cita, estado):
        """
        Actualiza una cita existente por su ID.
        """
        query = "UPDATE citas SET id_cliente = %s, id_barbero = %s, id_servicio = %s, fecha_cita = %s, hora_cita = %s, estado = %s WHERE id_cita = %s"
        return self.db.ejecutar_consulta(query, (id_cliente, id_barbero, id_servicio, fecha_cita, hora_cita, estado, id_cita))

    def eliminar_cita(self, id_cita):
        """
        Elimina una cita de la base de datos por su ID.
        """
        query = "DELETE FROM citas WHERE id_cita = %s"
        return self.db.ejecutar_consulta(query, (id_cita,))

    def cambiar_estado_cita(self, id_cita, nuevo_estado):
        """
        Cambia el estado de una cita.
        """
        query = "UPDATE citas SET estado = %s WHERE id_cita = %s"
        return self.db.ejecutar_consulta(query, (nuevo_estado, id_cita))