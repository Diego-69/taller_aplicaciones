from typing import Tuple
def insert_worker_with_user(data: Tuple[str, str, str, str, str, str, int, int, str, str]) -> Tuple[bool, str]:
    """
    Inserta un nuevo trabajador y su usuario en la base de datos.
    data: (rut, nombre, sexo, direccion, telefono, fecha_ingreso, id_cargo, id_depto, usuario, contrasena)
    """
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión"
    try:
        with conn.cursor() as cur:
            # Verificar que el nombre de usuario no exista
            cur.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s", (data[8],))
            if cur.fetchone() is not None:
                return False, "El nombre de usuario ya existe."
            # Insertar usuario
            import bcrypt
            contrasena_hash = bcrypt.hashpw(data[9].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            # Obtener id_perfil dinámicamente para 'Trabajador'
            cur.execute("SELECT id FROM perfiles WHERE nombre_perfil = %s", ('Trabajador',))
            perfil_row = cur.fetchone()
            if not perfil_row:
                return False, "No existe el perfil 'Trabajador' en la base de datos."
            id_perfil_trabajador = perfil_row[0]
            cur.execute("INSERT INTO usuarios (nombre_usuario, contrasena_hash, id_perfil) VALUES (%s, %s, %s) RETURNING id", (data[8], contrasena_hash, id_perfil_trabajador))
            res = cur.fetchone()
            if res is None:
                return False, "No se pudo crear el usuario."
            id_usuario = res[0]
            # Insertar trabajador
            cur.execute("""
                INSERT INTO trabajadores (rut, id_usuario, nombre_completo, sexo, direccion, telefono, fecha_ingreso, id_cargo, id_departamento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (data[0], id_usuario, data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
            conn.commit()
            return True, "Trabajador y usuario añadidos"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()
"""
Módulo de acceso a datos para El Correo de Yury.
Contiene funciones para conectar y consultar la base de datos PostgreSQL.
"""
import psycopg2
from PyQt6.QtWidgets import QMessageBox

DB_NAME = "correo_yury"
DB_USER = "ignacio"
DB_PASS = "ignacio123"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_db_connection():
    """Establece y retorna una conexión con la base de datos."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        QMessageBox.critical(None, "Error de Conexión", f"No se pudo conectar a la base de datos PostgreSQL.\nAsegúrate de que el servidor esté corriendo y la configuración sea correcta.\n\nError: {e}")
        return None

def get_all_workers(filtros=None):
    """Obtiene todos los trabajadores con su cargo y departamento."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            query = """
                SELECT t.rut, t.nombre_completo, t.sexo, t.direccion, t.telefono, t.fecha_ingreso, c.nombre_cargo, d.nombre_departamento, a.nombre_area
                FROM trabajadores t
                JOIN cargos c ON t.id_cargo = c.id
                JOIN departamentos d ON t.id_departamento = d.id
                JOIN areas a ON d.id_area = a.id
            """
            params = []
            if filtros:
                query += " WHERE " + filtros[0]
                params = filtros[1]
            cur.execute(query, params)
            return cur.fetchall()
    finally:
        conn.close()

def get_all_cargos():
    """Obtiene todos los cargos de la base de datos."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre_cargo FROM cargos ORDER BY nombre_cargo")
            return cur.fetchall()
    except Exception as e:
        print(f"Error al obtener cargos: {e}")
        return []
    finally:
        conn.close()

def get_all_departamentos():
    """Obtiene todos los departamentos de la base de datos."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre_departamento FROM departamentos ORDER BY nombre_departamento")
            return cur.fetchall()
    except Exception as e:
        print(f"Error al obtener departamentos: {e}")
        return []
    finally:
        conn.close()

def get_worker_by_rut(rut):
    """Obtiene los datos personales completos de un trabajador por su RUT, incluyendo ids de cargo y departamento."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            query = '''
                SELECT t.rut, t.nombre_completo, t.sexo, t.direccion, t.telefono, t.fecha_ingreso,
                       c.nombre_cargo, d.nombre_departamento, a.nombre_area, t.id_cargo, t.id_departamento
                FROM trabajadores t
                JOIN cargos c ON t.id_cargo = c.id
                JOIN departamentos d ON t.id_departamento = d.id
                JOIN areas a ON d.id_area = a.id
                WHERE t.rut = %s
            '''
            cur.execute(query, (rut,))
            return cur.fetchone()
    except Exception as e:
        print(f"Error al obtener datos del trabajador: {e}")
        return None
    finally:
        conn.close()

def insert_worker(data):
    """Inserta un nuevo trabajador en la base de datos."""
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión"
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO trabajadores (rut, nombre_completo, sexo, direccion, telefono, fecha_ingreso, id_cargo, id_departamento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, data)
            conn.commit()
            return True, "Trabajador añadido"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def update_worker(rut, data):
    """Actualiza los datos de un trabajador."""
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión"
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE trabajadores SET nombre_completo=%s, sexo=%s, direccion=%s, telefono=%s, fecha_ingreso=%s, id_cargo=%s, id_departamento=%s
                WHERE rut=%s
            """, (*data, rut))
            conn.commit()
            return True, "Trabajador actualizado"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def delete_worker(rut):
    """Elimina un trabajador por RUT."""
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión"
    try:
        with conn.cursor() as cur:
            # Obtener el id_usuario asociado al trabajador
            cur.execute("SELECT id_usuario FROM trabajadores WHERE rut = %s", (rut,))
            result = cur.fetchone()
            id_usuario = result[0] if result and result[0] else None
            # Eliminar trabajador
            cur.execute("DELETE FROM trabajadores WHERE rut = %s", (rut,))
            # Eliminar usuario si existe
            if id_usuario:
                cur.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
            conn.commit()
            return True, "Trabajador y usuario asociado eliminados"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def get_cargas_by_trabajador(rut):
    """Obtiene todas las cargas familiares de un trabajador."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, rut_carga, nombre_completo, parentesco, sexo FROM cargas_familiares WHERE trabajador_rut = %s", (rut,))
            return cur.fetchall()
    finally:
        conn.close()

def insert_carga(data):
    """Inserta una carga familiar."""
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión"
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cargas_familiares (rut_carga, trabajador_rut, nombre_completo, parentesco, sexo)
                VALUES (%s, %s, %s, %s, %s)
            """, data)
            conn.commit()
            return True, "Carga añadida"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def update_carga(id_carga, data):
    """Actualiza una carga familiar."""
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión"
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE cargas_familiares SET rut_carga=%s, nombre_completo=%s, parentesco=%s, sexo=%s
                WHERE id=%s
            """, (*data, id_carga))
            conn.commit()
            return True, "Carga actualizada"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def delete_carga(id_carga):
    """Elimina una carga familiar por ID."""
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión"
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cargas_familiares WHERE id = %s", (id_carga,))
            conn.commit()
            return True, "Carga eliminada"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def get_contactos_by_trabajador(rut):
    """Obtiene todos los contactos de emergencia de un trabajador."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre_completo, relacion, telefono FROM contactos_emergencia WHERE trabajador_rut = %s", (rut,))
            return cur.fetchall()
    finally:
        conn.close()

def insert_contacto(data):
    """Inserta un contacto de emergencia."""
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión"
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO contactos_emergencia (trabajador_rut, nombre_completo, relacion, telefono)
                VALUES (%s, %s, %s, %s)
            """, data)
            conn.commit()
            return True, "Contacto añadido"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def update_contacto(id_contacto, data):
    """Actualiza un contacto de emergencia."""
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión"
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE contactos_emergencia SET nombre_completo=%s, relacion=%s, telefono=%s
                WHERE id=%s
            """, (*data, id_contacto))
            conn.commit()
            return True, "Contacto actualizado"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def delete_contacto(id_contacto):
    """Elimina un contacto de emergencia por ID."""
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión"
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM contactos_emergencia WHERE id = %s", (id_contacto,))
            conn.commit()
            return True, "Contacto eliminado"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()
