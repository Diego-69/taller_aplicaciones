import psycopg2
import bcrypt
import getpass
from datetime import datetime
import os
import sys

DB_CONFIG = {
    'dbname': 'taller_apps',
    'user': 'ignacio',
    'password': 'ignacio123',
    'host': 'localhost', 
    'port': '5432',
    'client_encoding': 'latin1' 
}

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_banner():
    """Muestra un banner atractivo"""
    print("╔" + "═" * 60 + "╗")
    print("║" + " " * 15 + "🔐 GESTIÓN DE USUARIOS 🔐" + " " * 15 + "║")
    print("║" + " " * 20 + "Sistema de Taller Apps" + " " * 20 + "║")
    print("╚" + "═" * 60 + "╝")
    print()

def obtener_roles():
    """Obtiene los roles disponibles de la base de datos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM rol ORDER BY id")
        roles = cur.fetchall()
        cur.close()
        conn.close()
        return roles
    except psycopg2.Error as e:
        print(f"❌ Error al obtener roles: {e}")
        return []

def validar_rut(rut):
    """Valida formato básico de RUT chileno"""
    if not rut:
        return True  # RUT es opcional
    
    # Remover puntos y guiones
    rut_limpio = rut.replace(".", "").replace("-", "")
    
    # Verificar que tenga al menos 8 caracteres (7 números + 1 dígito verificador)
    if len(rut_limpio) < 8:
        return False
    
    # Verificar que los primeros caracteres sean números
    try:
        int(rut_limpio[:-1])
        return True
    except ValueError:
        return False

def crear_usuario_interactivo():
    """Permite crear usuarios de forma interactiva con validaciones"""
    try:
        print("\n" + "┌" + "─" * 50 + "┐")
        print("│" + " " * 15 + "🆕 CREAR NUEVO USUARIO" + " " * 15 + "│")
        print("└" + "─" * 50 + "┘")
        
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Mostrar roles disponibles
        roles = obtener_roles()
        if not roles:
            print("❌ No se pudieron cargar los roles.")
            return False
            
        print("\n📋 Roles disponibles:")
        print("┌" + "─" * 5 + "┬" + "─" * 20 + "┐")
        print("│ ID  │ Nombre             │")
        print("├" + "─" * 5 + "┼" + "─" * 20 + "┤")
        for rol_id, nombre in roles:
            print(f"│ {rol_id:<3} │ {nombre:<18} │")
        print("└" + "─" * 5 + "┴" + "─" * 20 + "┘")
        
        # Solicitar datos del usuario
        print("\n📝 Ingrese los datos del nuevo usuario:")
        
        # Username
        while True:
            username = input("👤 Nombre de usuario: ").strip()
            if not username:
                print("❌ El nombre de usuario no puede estar vacío.")
                continue
            
            # Verificar si el usuario ya existe
            cur.execute("SELECT username FROM usuario WHERE username = %s", (username,))
            if cur.fetchone():
                print("❌ El usuario ya existe. Elija otro nombre.")
                continue
            break
            
        # Password
        while True:
            password_plano = getpass.getpass("🔒 Contraseña: ")
            if not password_plano:
                print("❌ La contraseña no puede estar vacía.")
                continue
            if len(password_plano) < 4:
                print("❌ La contraseña debe tener al menos 4 caracteres.")
                continue
            
            confirm_password = getpass.getpass("🔒 Confirmar contraseña: ")
            if password_plano != confirm_password:
                print("❌ Las contraseñas no coinciden.")
                continue
            break
        
        # Rol
        while True:
            try:
                rol_id = int(input("👥 ID del rol: "))
                if not any(r[0] == rol_id for r in roles):
                    print("❌ ID de rol inválido.")
                    continue
                break
            except ValueError:
                print("❌ Debe ingresar un número válido.")
        
        # RUT trabajador (opcional)
        while True:
            rut_trabajador = input("🆔 RUT del trabajador (opcional, Enter para omitir): ").strip()
            if not rut_trabajador:
                rut_trabajador = None
                break
            
            if validar_rut(rut_trabajador):
                break
            else:
                print("❌ Formato de RUT inválido. Ejemplo: 12345678-9")

        # Confirmación
        print("\n📊 Resumen del usuario a crear:")
        print("┌" + "─" * 40 + "┐")
        print(f"│ Usuario: {username:<28} │")
        print(f"│ Rol ID: {rol_id:<30} │")
        print(f"│ RUT: {rut_trabajador or 'No especificado':<32} │")
        print("└" + "─" * 40 + "┘")
        
        confirmacion = input("\n¿Crear este usuario? (s/N): ").lower()
        if confirmacion != 's':
            print("❌ Creación cancelada.")
            return False

        # Hashear la contraseña
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_plano.encode('utf-8'), salt)

        # Insertar usuario
        cur.execute("""
            INSERT INTO usuario (username, password_hash, rol_id, rut_trabajador, activo, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, password_hash.decode('utf-8'), rol_id, rut_trabajador, True, datetime.now()))

        conn.commit()
        
        print("\n✅ Usuario creado exitosamente!")
        print(f"📋 Credenciales: {username} / {password_plano}")
        
        cur.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def crear_usuario_rrhh():
    """Mantiene la función original para crear usuario RRHH por defecto"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        username = 'rrhh.user'
        password_plano = '12345'

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_plano.encode('utf-8'), salt)

        cur.execute("""
            INSERT INTO usuario (username, password_hash, rol_id, rut_trabajador, activo, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (username) DO UPDATE
            SET password_hash = EXCLUDED.password_hash,
                fecha_creacion = EXCLUDED.fecha_creacion;
        """, (username, password_hash.decode('utf-8'), 2, None, True, datetime.now()))

        conn.commit()
        print(f"\n✅ Usuario '{username}' creado/actualizado exitosamente.")
        print(f"📋 Credenciales: {username} / {password_plano}")

        cur.close()
        conn.close()
        return True
    
    except psycopg2.Error as e:
        print(f"❌ Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def listar_usuarios():
    """Lista todos los usuarios existentes con formato mejorado"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT u.username, r.nombre, u.rut_trabajador, u.activo, u.fecha_creacion
            FROM usuario u
            JOIN rol r ON u.rol_id = r.id
            ORDER BY u.fecha_creacion DESC
        """)
        
        usuarios = cur.fetchall()
        
        print("\n" + "┌" + "─" * 50 + "┐")
        print("│" + " " * 15 + "👥 USUARIOS REGISTRADOS" + " " * 15 + "│")
        print("└" + "─" * 50 + "┘")
        
        if not usuarios:
            print("\n📭 No hay usuarios registrados.")
            return
        
        print("\n┌" + "─" * 20 + "┬" + "─" * 15 + "┬" + "─" * 15 + "┬" + "─" * 8 + "┬" + "─" * 20 + "┐")
        print("│ Usuario            │ Rol           │ RUT           │ Activo │ Fecha Creación     │")
        print("├" + "─" * 20 + "┼" + "─" * 15 + "┼" + "─" * 15 + "┼" + "─" * 8 + "┼" + "─" * 20 + "┤")
        
        for username, rol, rut, activo, fecha in usuarios:
            rut_str = rut if rut else "N/A"
            activo_str = "✅ Sí" if activo else "❌ No"
            fecha_str = fecha.strftime('%d/%m/%Y %H:%M') if fecha else "N/A"
            
            print(f"│ {username:<18} │ {rol:<13} │ {rut_str:<13} │ {activo_str:<6} │ {fecha_str:<18} │")
        
        print("└" + "─" * 20 + "┴" + "─" * 15 + "┴" + "─" * 15 + "┴" + "─" * 8 + "┴" + "─" * 20 + "┘")
        print(f"\n📊 Total de usuarios: {len(usuarios)}")
        
        cur.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error al listar usuarios: {e}")

def eliminar_usuario():
    """Permite eliminar un usuario existente"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("\n" + "┌" + "─" * 50 + "┐")
        print("│" + " " * 15 + "🗑️  ELIMINAR USUARIO" + " " * 16 + "│")
        print("└" + "─" * 50 + "┘")
        
        # Mostrar usuarios existentes
        cur.execute("SELECT username FROM usuario ORDER BY username")
        usuarios = cur.fetchall()
        
        if not usuarios:
            print("\n📭 No hay usuarios para eliminar.")
            return
        
        print("\n👥 Usuarios existentes:")
        for i, (username,) in enumerate(usuarios, 1):
            print(f"{i}. {username}")
        
        # Solicitar usuario a eliminar
        username = input("\n👤 Nombre del usuario a eliminar: ").strip()
        
        # Verificar que existe
        cur.execute("SELECT username FROM usuario WHERE username = %s", (username,))
        if not cur.fetchone():
            print("❌ El usuario no existe.")
            return
        
        # Confirmación
        confirmacion = input(f"⚠️  ¿Está seguro de eliminar el usuario '{username}'? (s/N): ").lower()
        if confirmacion != 's':
            print("❌ Eliminación cancelada.")
            return
        
        # Eliminar usuario
        cur.execute("DELETE FROM usuario WHERE username = %s", (username,))
        conn.commit()
        
        print(f"✅ Usuario '{username}' eliminado exitosamente.")
        
        cur.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error al eliminar usuario: {e}")

def mostrar_estadisticas():
    """Muestra estadísticas del sistema"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("\n" + "┌" + "─" * 50 + "┐")
        print("│" + " " * 15 + "📊 ESTADÍSTICAS" + " " * 19 + "│")
        print("└" + "─" * 50 + "┘")
        
        # Total usuarios
        cur.execute("SELECT COUNT(*) FROM usuario")
        total_usuarios = cur.fetchone()[0]
        
        # Usuarios activos
        cur.execute("SELECT COUNT(*) FROM usuario WHERE activo = true")
        usuarios_activos = cur.fetchone()[0]
        
        # Usuarios por rol
        cur.execute("""
            SELECT r.nombre, COUNT(u.id) 
            FROM rol r 
            LEFT JOIN usuario u ON r.id = u.rol_id 
            GROUP BY r.id, r.nombre 
            ORDER BY r.nombre
        """)
        usuarios_por_rol = cur.fetchall()
        
        print(f"\n📈 Resumen general:")
        print(f"   👥 Total usuarios: {total_usuarios}")
        print(f"   ✅ Usuarios activos: {usuarios_activos}")
        print(f"   ❌ Usuarios inactivos: {total_usuarios - usuarios_activos}")
        
        print(f"\n👔 Usuarios por rol:")
        for rol, cantidad in usuarios_por_rol:
            print(f"   📋 {rol}: {cantidad} usuarios")
        
        cur.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error al obtener estadísticas: {e}")

def menu_principal():
    """Muestra el menú principal con opciones mejoradas"""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        
        print("📋 OPCIONES DISPONIBLES:")
        print("┌" + "─" * 50 + "┐")
        print("│ 1. 🆕 Crear usuario personalizado           │")
        print("│ 2. 👤 Crear usuario RRHH por defecto       │")
        print("│ 3. 👥 Listar usuarios existentes           │")
        print("│ 4. 🗑️  Eliminar usuario                     │")
        print("│ 5. 📊 Ver estadísticas                     │")
        print("│ 6. 🚪 Salir                                │")
        print("└" + "─" * 50 + "┘")
        
        try:
            opcion = input("\n🎯 Seleccione una opción (1-6): ").strip()
            
            if opcion == "1":
                crear_usuario_interactivo()
                input("\n⏎ Presione Enter para continuar...")
                
            elif opcion == "2":
                crear_usuario_rrhh()
                input("\n⏎ Presione Enter para continuar...")
                
            elif opcion == "3":
                listar_usuarios()
                input("\n⏎ Presione Enter para continuar...")
                
            elif opcion == "4":
                eliminar_usuario()
                input("\n⏎ Presione Enter para continuar...")
                
            elif opcion == "5":
                mostrar_estadisticas()
                input("\n⏎ Presione Enter para continuar...")
                
            elif opcion == "6":
                print("\n👋 ¡Hasta luego!")
                sys.exit(0)
                
            else:
                print("❌ Opción inválida. Intente nuevamente.")
                input("\n⏎ Presione Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saliendo del programa...")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("\n⏎ Presione Enter para continuar...")

if __name__ == '__main__':
    menu_principal()