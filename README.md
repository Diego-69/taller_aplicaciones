# El Correo de Yury - Gestión de Recursos Humanos

Aplicación de escritorio para la gestión de trabajadores, cargas familiares y contactos de emergencia en la empresa "El Correo de Yury". Desarrollada en Python con PyQt6 y PostgreSQL.

---

## Características principales

- **Login seguro** con perfiles: Admin, RRHH y Trabajador.
- **Registro de trabajadores** desde la ventana de login.
- **CRUD completo** para trabajadores, cargas familiares y contactos de emergencia.
- **Gestión de perfiles** y roles de usuario.
- **Validaciones** de datos (RUT, teléfono, campos obligatorios).
- **Documentación y manuales** incluidos.
- **Estructura modular** y modelo en n-capas para fácil mantenimiento.

---

## Estructura del proyecto

```
eva4_tallerApps/
│
├── main.py
├── requirements.txt
├── schema.sql
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── logic.py
│   ├── ui_login.py
│   ├── ui_main_window.py
│   ├── ui_register.py
│   └── docs/
│       ├── MANUAL_USUARIO.md
│       ├── MANUAL_INSTALACION.md
│       └── TERMINOS_Y_CONDICIONES.md
│
├── test/
│   └── PRUEBAS.md
```

---

## Instalación rápida

1. **Clona el repositorio** o descarga los archivos.
2. **Crea y activa un entorno virtual** (opcional pero recomendado):

   ```sh
   python -m venv venv
   venv\Scripts\activate   # En Windows
   ```

3. **Instala las dependencias**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Configura la base de datos**:
   - Crea una base de datos PostgreSQL llamada `correo_yury`.
   - Ejecuta el script `schema.sql` para crear las tablas y datos iniciales.

5. **Configura la conexión** en `app/database.py` si es necesario (usuario, contraseña, host, etc).

6. **Ejecuta la aplicación**:

   ```sh
   python main.py
   ```

---

## Primeros pasos

- Inicia sesión con el usuario inicial:
  - **Usuario:** `admin_rrhh`
  - **Contraseña:** `admin123`
  - **Perfil:** RRHH

- Los trabajadores pueden registrarse desde el botón "Registrarse" en la ventana de login.

---

## Manuales y documentación

- [Manual de Usuario](app/docs/MANUAL_USUARIO.md)
- [Manual de Instalación](app/docs/MANUAL_INSTALACION.md)
- [Términos y Condiciones](app/docs/TERMINOS_Y_CONDICIONES.md)
- [Casos de Prueba](test/PRUEBAS.md)

---

## Tecnologías utilizadas

- Python 3.x
- PyQt6
- PostgreSQL
- psycopg2
- bcrypt

---

## Estructura de la base de datos

Consulta el archivo [`schema.sql`](schema.sql) para ver la estructura completa y los datos iniciales.

---

## Contribuciones

Si deseas mejorar la aplicación, puedes crear un fork y enviar un pull request.  
Para reportar errores o sugerencias, utiliza el sistema de issues del repositorio.

---

## Licencia

Este proyecto es de uso interno para "El Correo de Yury". Consulta [Términos y Condiciones](app/docs/TERMINOS_Y_CONDICIONES.md).

---

**Desarrollado por:**  
Ygnac - 2025
