# barberia_app/modelo_db.py
import mysql.connector
from mysql.connector import Error

class ModelDB:
    """
    Clase para manejar la conexión y operaciones básicas con la base de datos MariaDB.
    """
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None # Conexión a la base de datos
        self.cursor = None # Cursor para ejecutar consultas

    def conectar(self):
        """
        Establece la conexión con la base de datos.
        """
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.conn.is_connected():
                print(f"Conexión exitosa a la base de datos '{self.database}'")
                self.cursor = self.conn.cursor(dictionary=True) # dictionary=True para obtener resultados como diccionarios
                return True
        except Error as e:
            print(f"Error al conectar a MariaDB: {e}")
            return False
        return False

    def desconectar(self):
        """
        Cierra la conexión con la base de datos.
        """
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Conexión a la base de datos cerrada.")

    def ejecutar_consulta(self, query, params=None):
        """
        Ejecuta una consulta SQL (SELECT, INSERT, UPDATE, DELETE).
        Retorna los resultados para SELECT, y True/False para otras operaciones.
        """
        try:
            if not self.conn or not self.conn.is_connected():
                if not self.conectar():
                    return False

            self.cursor.execute(query, params or ())
            if query.strip().upper().startswith("SELECT"):
                result = self.cursor.fetchall()
                return result
            else:
                self.conn.commit()
                return True
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            self.conn.rollback() # Deshace cambios si hay un error
            return False

    def obtener_ultimo_id(self):
        """
        Retorna el ID del último registro insertado. Útil para operaciones INSERT.
        """
        return self.cursor.lastrowid

# Ejemplo de uso (para probar la conexión y la clase)
if __name__ == "__main__":
    # Configura tus credenciales de MariaDB aquí
    db_config = {
        'host': 'localhost',
        'database': 'barberia_db',
        'user': 'root',
        'password': 'tu_contrasena_root' # ¡CUIDADO! CAMBIA ESTO POR TU CONTRASEÑA REAL DE ROOT DE MARIA DB
    }

    db_model = ModelDB(**db_config)

    if db_model.conectar():
        print("Conexión de prueba establecida.")

        # Prueba de inserción
        # query_insert = "INSERT INTO clientes (nombre, apellido, telefono) VALUES (%s, %s, %s)"
        # params_insert = ("Juan", "Pérez", "123456789")
        # if db_model.ejecutar_consulta(query_insert, params_insert):
        #     print(f"Cliente insertado con ID: {db_model.obtener_ultimo_id()}")
        # else:
        #     print("No se pudo insertar el cliente.")

        # Prueba de consulta
        query_select = "SELECT * FROM usuarios"
        usuarios = db_model.ejecutar_consulta(query_select)
        if usuarios:
            print("\nUsuarios en la base de datos:")
            for usuario in usuarios:
                print(usuario)
        else:
            print("No se encontraron usuarios o hubo un error.")

        db_model.desconectar()
    else:
        print("No se pudo conectar a la base de datos.")