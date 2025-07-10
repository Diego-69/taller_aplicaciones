# Manual de Instalación - El Correo de Yury

## Requisitos Previos
- Python 3.x
- PostgreSQL

## Instalación de la Base de Datos
1. Crear la base de datos `correo_yury` en PostgreSQL.
2. Ejecutar el script `schema.sql` para crear las tablas y datos iniciales.

## Instalación de la Aplicación
1. Clonar el repositorio o copiar los archivos.
2. Crear y activar un entorno virtual:
   - `python -m venv venv`
   - `venv\Scripts\activate` (Windows)
3. Instalar dependencias:
   - `pip install -r requirements.txt`

## Configuración
- Editar los datos de conexión a la base de datos en `database.py` si es necesario.

## Ejecución
- Ejecutar la aplicación con:
  - `python main.py`
