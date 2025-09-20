# barberia_app/models/modelo_usuario.py
from core.modelo_db import ModelDB

class ModeloUsuario:
    """
    Gestiona las operaciones de base de datos para los usuarios.
    """
    def __init__(self, db_config):
        self.db = ModelDB(**db_config)

    def autenticar_usuario(self, nombre_usuario, contrasena):
        """
        Autentica un usuario verificando su nombre de usuario y contraseña.
        Retorna el rol del usuario si la autenticación es exitosa, None en caso contrario.
        """
        query = "SELECT rol, contrasena FROM usuarios WHERE nombre_usuario = %s"
        usuario_db = self.db.ejecutar_consulta(query, (nombre_usuario,))

        if usuario_db:
            # Como se acordó, no encriptamos para la prueba
            if usuario_db[0]['contrasena'] == contrasena:
                return usuario_db[0]['rol']
        return None

    def obtener_usuarios(self):
        """
        Obtiene todos los usuarios de la base de datos.
        """
        query = "SELECT id_usuario, nombre_usuario, rol FROM usuarios"
        return self.db.ejecutar_consulta(query)

    def agregar_usuario(self, nombre_usuario, contrasena, rol):
        """
        Agrega un nuevo usuario a la base de datos.
        """
        query = "INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES (%s, %s, %s)"
        return self.db.ejecutar_consulta(query, (nombre_usuario, contrasena, rol))

    def actualizar_usuario(self, id_usuario, nombre_usuario, contrasena, rol):
        """
        Actualiza un usuario existente por su ID.
        """
        query = "UPDATE usuarios SET nombre_usuario = %s, contrasena = %s, rol = %s WHERE id_usuario = %s"
        return self.db.ejecutar_consulta(query, (nombre_usuario, contrasena, rol, id_usuario))

    def eliminar_usuario(self, id_usuario):
        """
        Elimina un usuario de la base de datos por su ID.
        """
        query = "DELETE FROM usuarios WHERE id_usuario = %s"
        return self.db.ejecutar_consulta(query, (id_usuario,))

    def actualizar_usuario_por_nombre(self, nombre_usuario, nueva_contrasena):
        """
        Cambia la contraseña de un usuario por su nombre de usuario.
        """
        query = "UPDATE usuarios SET contrasena = %s WHERE nombre_usuario = %s"
        return self.db.ejecutar_consulta(query, (nueva_contrasena, nombre_usuario))