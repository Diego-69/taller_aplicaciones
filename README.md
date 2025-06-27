<<<<<<< HEAD
Sistema de Gestión de Recursos Humanos - "El Correo de Yury"
Este proyecto es una aplicación de escritorio desarrollada en Python para la gestión de la nómina y los datos de los trabajadores de la empresa "El Correo de Yury". La aplicación centraliza la información de los empleados, automatiza tareas de RR.HH. y ofrece un portal de autoservicio para los trabajadores, reemplazando la gestión manual a través de planillas Excel.

✨ Características Principales
Autenticación Segura: Inicio de sesión basado en roles de usuario con contraseñas encriptadas (hashed).

Gestión de Trabajadores:

Listado completo de trabajadores activos en una tabla resumen.

Creación, visualización y edición de la ficha completa del trabajador (datos personales, laborales, contactos de emergencia y cargas familiares).

Acceso Basado en Roles:

Personal de RR.HH.: Puede gestionar la información de todos los trabajadores.

Jefe de RR.HH.: Tiene acceso a herramientas de filtrado avanzadas para generar reportes específicos.

Trabajador: Puede visualizar su propia información y modificar sus datos personales, contactos y cargas familiares.

Filtros Avanzados: Herramientas para que la jefatura de RR.HH. pueda filtrar el listado de trabajadores por sexo, cargo, área y departamento.

Portal de Autoservicio: Permite a los empleados gestionar su propia información personal, reduciendo la carga administrativa del equipo de RR.HH.

🛠️ Tecnologías Utilizadas
Lenguaje de Programación: Python 3

Interfaz Gráfica (GUI): PyQt6

Base de Datos: PostgreSQL

Conector de Base de Datos: psycopg2-binary

Encriptación de Contraseñas: bcrypt

🚀 Instalación y Configuración
Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

1. Requisitos Previos
Tener instalado Python 3.8 o superior.

Tener instalado y en ejecución un servidor de PostgreSQL.

2. Configuración del Entorno
# 1. Clona este repositorio en tu máquina local
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio

# 2. Crea un entorno virtual para el proyecto
python -m venv venv

# 3. Activa el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# 4. Instala todas las dependencias necesarias
pip install -r requirements.txt

3. Configuración de la Base de Datos
Crea una nueva base de datos en PostgreSQL para el proyecto (ej. correo_yury_db).

Ejecuta el script schema.sql (el que contiene todas las sentencias CREATE TABLE e INSERT) en tu base de datos para crear la estructura de tablas y cargar los datos iniciales.

Abre los archivos app_nomina.py y crear_usuario.py en tu editor de código.

Modifica el diccionario DB_CONFIG en ambos archivos con tus credenciales de conexión a PostgreSQL (nombre de la base de datos, usuario, contraseña, etc.).

4. Creación del Usuario Inicial
La base de datos se crea con contraseñas de ejemplo que no son funcionales. Para poder iniciar sesión, debes crear un usuario con una contraseña real.

# Ejecuta este script UNA VEZ para crear el usuario 'rrhh.user'
# con la contraseña '12345'.
python crear_usuario.py

▶️ Uso de la Aplicación
Una vez completada la instalación y configuración:

Asegúrate de que tu entorno virtual esté activado.

Ejecuta la aplicación principal:

python app_nomina.py

Se abrirá la ventana de inicio de sesión. Ingresa con las siguientes credenciales:

Usuario: rrhh.user

Contraseña: 12345

¡Listo! Ya puedes empezar a utilizar el sistema.

Proyecto desarrollado como solución a las necesidades de gestión de personal de "El Correo de Yury".
=======
# Proyecto final de la asignatura Taller de Aplicaciones
>>>>>>> 2bc454a3438034655e6752893789749b3690082d
