import psycopg2
import bcrypt

DB_CONFIG = {
    'dbname': 'taller_apps',
    'user': 'ignacio',
    'password': 'ignacio123',
    'host': 'localhost', 
    'port': '5432',
    'client_encoding': 'latin1' 
}

def crear_usuario_rrhh():
    """
    Inserta un usuario de RR.HH. con una contraseña hasheada para poder probar la aplicación.
    El rol 'rrhh' tiene id=2 según tu script SQL.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        username = 'rrhh.user'
        password_plano = '12345'

        # Hashear la contraseña con bcrypt
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_plano.encode('utf-8'), salt)

        # Insertar el nuevo usuario o actualizar la contraseña si el usuario ya existe.
        # El rol de 'rrhh' es 2.
        # No se asocia a un rut_trabajador porque es un rol de gestión general.
        cur.execute("""
            INSERT INTO usuario (username, password_hash, rol_id, rut_trabajador, activo)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (username) DO UPDATE
            SET password_hash = EXCLUDED.password_hash;
        """, (username, password_hash.decode('utf-8'), 2, None, True))

        # Confirma la transacción
        conn.commit()
        print(f"Usuario '{username}' creado/actualizado exitosamente.")
        print(f"Puedes iniciar sesión con usuario: {username} y contraseña: {password_plano}")

        cur.close()
        conn.close()
    
    except psycopg2.Error as e:
        print(f"Error al conectar o al interactuar con la base de datos: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


if __name__ == '__main__':
    crear_usuario_rrhh()
