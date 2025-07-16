"""
Capa de lógica de negocio para El Correo de Yury.
Contiene funciones que procesan datos y coordinan la lógica entre la UI y la base de datos.
"""
import bcrypt
from app.database import get_db_connection

def autenticar_usuario(username, password):
    """Verifica las credenciales del usuario y retorna su perfil y RUT."""
    conn = get_db_connection()
    if not conn:
        return None, None
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT u.contrasena_hash, p.nombre_perfil, t.rut "
                "FROM usuarios u "
                "JOIN perfiles p ON u.id_perfil = p.id "
                "LEFT JOIN trabajadores t ON u.id = t.id_usuario "
                "WHERE u.nombre_usuario = %s", (username,)
            )
            user_data = cur.fetchone()
            if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[0].encode('utf-8')):
                return user_data[1], user_data[2]
    except Exception:
        pass
    finally:
        if conn:
            conn.close()
    return None, None

def registrar_trabajador(data):
    """
    Registra un nuevo usuario con perfil Trabajador y lo asocia a un trabajador.
    data: dict con username, password, rut, nombre, sexo, direccion, telefono
    """
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión"
    try:
        with conn.cursor() as cur:
            # Verifica si el usuario o el RUT ya existen
            cur.execute("SELECT 1 FROM usuarios WHERE nombre_usuario = %s", (data["username"],))
            if cur.fetchone():
                return False, "El nombre de usuario ya existe."
            cur.execute("SELECT 1 FROM trabajadores WHERE rut = %s", (data["rut"],))
            if cur.fetchone():
                return False, "El RUT ya está registrado."

            # Obtiene el id del perfil Trabajador
            cur.execute("SELECT id FROM perfiles WHERE nombre_perfil = 'Trabajador'")
            perfil_row = cur.fetchone()
            if not perfil_row:
                return False, "No existe el perfil Trabajador"
            id_perfil = perfil_row[0]
            # Hashea la contraseña
            import bcrypt
            hash_pw = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            # Inserta el usuario
            cur.execute(
                "INSERT INTO usuarios (nombre_usuario, contrasena_hash, id_perfil) VALUES (%s, %s, %s) RETURNING id",
                (data["username"], hash_pw, id_perfil)
            )
            id_usuario = cur.fetchone()[0]
            # Inserta el trabajador (por defecto cargo=1, departamento=1, puedes ajustar esto)
            # Se asume que el registro de trabajador no asigna cargo ni depto inicialmente.
            # Esto debería ser completado por RRHH.
            cur.execute(
                "INSERT INTO trabajadores (rut, id_usuario, nombre_completo, sexo, direccion, telefono, fecha_ingreso, id_cargo, id_departamento) "
                "VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE, 1, 1)", # IDs por defecto
                (data["rut"], id_usuario, data["nombre"], data["sexo"], data["direccion"], data["telefono"])
            )
            conn.commit()
            return True, "Usuario registrado correctamente. Un administrador de RRHH asignará su cargo y departamento."
    except Exception as e:
        conn.rollback()
        # Evitar exponer detalles de la base de datos en producción
        print(f"Error en registro: {e}") # Log para depuración
        return False, "Ocurrió un error inesperado durante el registro."
    finally:
        conn.close()
