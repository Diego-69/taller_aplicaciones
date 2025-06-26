import sys
import psycopg2
import bcrypt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel,
    QMessageBox, QDialog, QFormLayout, QComboBox, QTabWidget,
    QGroupBox, QHeaderView
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

# --- CONFIGURA TUS DATOS DE CONEXIÓN A POSTGRESQL AQUÍ ---
DB_CONFIG = {
    'dbname': 'taller_apps',
    'user': 'ignacio',
    'password': 'ignacio123',
    'host': 'localhost',
    'port': '5432'
}

class DatabaseManager:
    """
    Clase para manejar todas las interacciones con la base de datos PostgreSQL.
    """
    def __init__(self):    
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
        except psycopg2.OperationalError as e:
            # Este error es crítico, se muestra al iniciar.
            self.show_critical_error(f"No se pudo conectar a la base de datos:\n{e}")
            sys.exit(1) # Cierra la aplicación si no hay conexión

    def show_critical_error(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText("Error de Conexión")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Error Crítico")
        msg_box.exec()

    def check_user(self, username, password):
        """
        Verifica las credenciales del usuario contra la base de datos.
        Devuelve la información del usuario si es exitoso, de lo contrario None.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT u.id, u.password_hash, u.rol_id, r.nombre, u.rut_trabajador
                FROM usuario u
                JOIN rol r ON u.rol_id = r.id
                WHERE u.username = %s AND u.activo = TRUE
            """, (username,))
            user_data = cur.fetchone()

            if user_data:
                user_id, hashed_password, role_id, role_name, worker_rut = user_data
                # Verificar la contraseña
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    self.log_access(user_id, True)
                    return {'id': user_id, 'role_id': role_id, 'role_name': role_name, 'worker_rut': worker_rut}
            
            # Si el usuario existe pero la contraseña es incorrecta, o no existe
            if user_data:
                self.log_access(user_data[0], False) # Log de intento fallido
            return None

    def log_access(self, user_id, success):
        """Registra un intento de inicio de sesión en la tabla log_acceso."""
        with self.conn.cursor() as cur:
            # IP no se captura en esta versión, se deja como NULL
            cur.execute("""
                INSERT INTO log_acceso (usuario_id, exito, ip_origen)
                VALUES (%s, %s, %s)
            """, (user_id, success, '127.0.0.1'))
            self.conn.commit()

    def get_workers_summary(self, filters=None):
        """
        Obtiene un listado resumen de los trabajadores.
        Puede aplicar filtros para la vista del Jefe de RR.HH.
        """
        query = """
            SELECT t.rut, t.nombre, t.sexo, dl.cargo
            FROM trabajador t
            JOIN datos_laborales dl ON t.rut = dl.rut_trabajador
            WHERE dl.estado = 'activo'
        """
        params = []
        if filters:
            conditions = []
            if filters.get('sexo'):
                conditions.append("t.sexo = %s")
                params.append(filters['sexo'])
            if filters.get('cargo'):
                conditions.append("dl.cargo ILIKE %s")
                params.append(f"%{filters['cargo']}%")
            if filters.get('area_id'):
                conditions.append("dl.area_id = %s")
                params.append(filters['area_id'])
            if filters.get('departamento_id'):
                conditions.append("dl.departamento_id = %s")
                params.append(filters['departamento_id'])

            if conditions:
                query += " AND " + " AND ".join(conditions)

        with self.conn.cursor() as cur:
            cur.execute(query, tuple(params))
            return cur.fetchall()

    def get_areas(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, nombre FROM area ORDER BY nombre")
            return cur.fetchall()
            
    def get_departments_by_area(self, area_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, nombre FROM departamento WHERE area_id = %s ORDER BY nombre", (area_id,))
            return cur.fetchall()
            
    def get_all_departments(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, nombre FROM departamento ORDER BY nombre")
            return cur.fetchall()

    def get_worker_details(self, rut):
        """Obtiene todos los detalles de un trabajador para el formulario."""
        details = {}
        with self.conn.cursor() as cur:
            # Datos personales
            cur.execute("SELECT nombre, sexo, direccion, telefono, fecha_nacimiento, email FROM trabajador WHERE rut = %s", (rut,))
            details['personal'] = cur.fetchone()
            # Datos laborales
            cur.execute("SELECT cargo, fecha_de_ingreso, area_id, departamento_id FROM datos_laborales WHERE rut_trabajador = %s", (rut,))
            details['laboral'] = cur.fetchone()
            # Contactos de emergencia
            cur.execute("SELECT nombre_contacto, relacion, telefono_contacto FROM contactos_emergencia WHERE rut_trabajador = %s", (rut,))
            details['emergencia'] = cur.fetchall()
            # Cargas familiares
            cur.execute("SELECT nombre, parentesco, sexo, rut FROM cargas_familiares WHERE rut_trabajador = %s", (rut,))
            details['cargas'] = cur.fetchall()
        return details

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()

class LoginWindow(QDialog):
    """Ventana de diálogo para el inicio de sesión."""
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.user_info = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Inicio de Sesión - El Correo de Yury")
        self.setFixedSize(350, 200)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Usuario:", self.username_input)
        form_layout.addRow("Contraseña:", self.password_input)

        self.login_button = QPushButton("Ingresar", self)
        self.login_button.clicked.connect(self.handle_login)

        layout.addLayout(form_layout)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "El usuario y la contraseña no pueden estar vacíos.")
            return

        user_info = self.db_manager.check_user(username, password)
        if user_info:
            self.user_info = user_info
            self.accept() # Cierra el diálogo con éxito
        else:
            QMessageBox.warning(self, "Error de Autenticación", "Usuario o contraseña incorrectos.")


class MainWindow(QMainWindow):
    """Ventana Principal de la aplicación."""
    def __init__(self, db_manager, user_info):
        super().__init__()
        self.db_manager = db_manager
        self.user_info = user_info
        
        # Diccionarios para guardar mapeos de id -> nombre
        self.areas_map = {id: name for id, name in self.db_manager.get_areas()}
        self.depts_map = {id: name for id, name in self.db_manager.get_all_departments()}

        self.initUI()
        self.load_initial_data()

    def initUI(self):
        self.setWindowTitle(f"SIGERH - El Correo de Yury (Usuario: {self.user_info['role_name']})")
        self.setGeometry(100, 100, 1200, 700)
        
        # El widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)

        # Determinar la interfaz según el rol
        # Roles 'admin', 'jefe_rrhh', 'rrhh' tienen la misma vista de gestión
        if self.user_info['role_name'] in ['admin', 'jefe_rrhh', 'rrhh']:
            self.setup_hr_ui()
        elif self.user_info['role_name'] == 'trabajador':
            self.setup_worker_ui()

    def setup_hr_ui(self):
        """Configura la interfaz para usuarios de RR.HH."""
        # Panel de filtros
        filter_group = QGroupBox("Filtros de Búsqueda")
        filter_layout = QFormLayout()

        self.sexo_filter = QComboBox()
        self.sexo_filter.addItems(["Todos", "Masculino", "Femenino"])
        
        self.cargo_filter = QLineEdit()

        self.area_filter = QComboBox()
        self.area_filter.addItem("Todas", None)
        for area_id, area_name in self.areas_map.items():
            self.area_filter.addItem(area_name, area_id)

        self.depto_filter = QComboBox()
        self.depto_filter.addItem("Todos", None)

        # Conectar señal de área para actualizar departamentos
        self.area_filter.currentIndexChanged.connect(self.update_department_filter)

        filter_layout.addRow("Sexo:", self.sexo_filter)
        filter_layout.addRow("Cargo:", self.cargo_filter)
        filter_layout.addRow("Área:", self.area_filter)
        filter_layout.addRow("Departamento:", self.depto_filter)

        self.filter_button = QPushButton("Filtrar")
        self.clear_button = QPushButton("Limpiar Filtros")
        
        # Solo el jefe de RRHH puede filtrar
        is_jefe = self.user_info['role_name'] == 'jefe_rrhh'
        filter_group.setVisible(is_jefe)
        self.filter_button.setVisible(is_jefe)
        self.clear_button.setVisible(is_jefe)
        
        self.filter_button.clicked.connect(self.apply_filters)
        self.clear_button.clicked.connect(self.clear_filters)

        filter_vbox = QVBoxLayout()
        filter_vbox.addWidget(filter_group)
        filter_vbox.addLayout(filter_layout)
        filter_vbox.addWidget(self.filter_button)
        filter_vbox.addWidget(self.clear_button)
        filter_vbox.addStretch()

        # Tabla de trabajadores
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["RUT", "Nombre", "Sexo", "Cargo"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Botones de acción
        self.add_button = QPushButton("Agregar Trabajador")
        self.edit_button = QPushButton("Ver/Editar Ficha")
        self.delete_button = QPushButton("Dar de Baja") # Lógica de 'estado'
        
        action_layout = QHBoxLayout()
        action_layout.addWidget(self.add_button)
        action_layout.addWidget(self.edit_button)
        action_layout.addWidget(self.delete_button)
        
        # Panel derecho (tabla y acciones)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.table)
        right_layout.addLayout(action_layout)
        
        # Añadir paneles al layout principal
        self.main_layout.addLayout(filter_vbox, 1) # Filtros ocupan 1/4 del espacio
        self.main_layout.addLayout(right_layout, 3) # Tabla ocupa 3/4

    def update_department_filter(self):
        self.depto_filter.clear()
        self.depto_filter.addItem("Todos", None)
        area_id = self.area_filter.currentData()
        if area_id:
            departments = self.db_manager.get_departments_by_area(area_id)
            for dept_id, dept_name in departments:
                self.depto_filter.addItem(dept_name, dept_id)
                
    def apply_filters(self):
        filters = {}
        if self.sexo_filter.currentIndex() > 0:
            filters['sexo'] = self.sexo_filter.currentText()
        if self.cargo_filter.text():
            filters['cargo'] = self.cargo_filter.text()
        if self.area_filter.currentData():
            filters['area_id'] = self.area_filter.currentData()
        if self.depto_filter.currentData():
            filters['departamento_id'] = self.depto_filter.currentData()
            
        self.load_workers_data(filters)

    def clear_filters(self):
        self.sexo_filter.setCurrentIndex(0)
        self.cargo_filter.clear()
        self.area_filter.setCurrentIndex(0)
        self.depto_filter.setCurrentIndex(0)
        self.load_workers_data()

    def setup_worker_ui(self):
        """Configura la interfaz para un trabajador regular."""
        rut = self.user_info.get('worker_rut')
        if not rut:
            self.main_layout.addWidget(QLabel("Este usuario no está asociado a ningún trabajador."))
            return
            
        worker_data = self.db_manager.get_worker_details(rut)
        
        main_form_layout = QFormLayout()
        
        # Pestañas para organizar la información
        tabs = QTabWidget()
        
        # Pestaña 1: Datos Personales
        personal_tab = QWidget()
        personal_layout = QFormLayout(personal_tab)
        self.w_nombre = QLineEdit(worker_data['personal'][0])
        self.w_rut = QLineEdit(rut)
        self.w_rut.setReadOnly(True) # RUT no se puede modificar
        self.w_sexo = QLineEdit(worker_data['personal'][1])
        self.w_sexo.setReadOnly(True) # Sexo tampoco debería ser modificable por el empleado
        self.w_direccion = QLineEdit(worker_data['personal'][2])
        self.w_telefono = QLineEdit(worker_data['personal'][3])
        
        personal_layout.addRow("Nombre Completo:", self.w_nombre)
        personal_layout.addRow("RUT:", self.w_rut)
        personal_layout.addRow("Sexo:", self.w_sexo)
        personal_layout.addRow("Dirección:", self.w_direccion)
        personal_layout.addRow("Teléfono:", self.w_telefono)
        tabs.addTab(personal_tab, "Datos Personales")

        # Pestaña 2: Datos Laborales (solo lectura)
        laboral_tab = QWidget()
        laboral_layout = QFormLayout(laboral_tab)
        
        cargo = QLineEdit(worker_data['laboral'][0])
        fecha_ingreso = QLineEdit(str(worker_data['laboral'][1]))
        area = QLineEdit(self.areas_map.get(worker_data['laboral'][2]))
        depto = QLineEdit(self.depts_map.get(worker_data['laboral'][3]))
        
        for field in [cargo, fecha_ingreso, area, depto]:
            field.setReadOnly(True)

        laboral_layout.addRow("Cargo:", cargo)
        laboral_layout.addRow("Fecha Ingreso:", fecha_ingreso)
        laboral_layout.addRow("Área:", area)
        laboral_layout.addRow("Departamento:", depto)
        tabs.addTab(laboral_tab, "Datos Laborales")

        # Pestaña 3: Contactos de Emergencia y Cargas (Modificable)
        # En una app real, esto sería más complejo con tablas y botones add/remove
        # Por simplicidad, se muestra como editable.
        contacts_tab = QWidget()
        # ... Lógica para mostrar y editar contactos y cargas
        tabs.addTab(contacts_tab, "Contactos y Cargas")

        self.save_button = QPushButton("Guardar Cambios")
        # self.save_button.clicked.connect(self.save_worker_changes)
        
        self.main_layout.addWidget(tabs)
        self.main_layout.addWidget(self.save_button)
        
    def load_initial_data(self):
        """Carga los datos iniciales al abrir la ventana."""
        if self.user_info['role_name'] != 'trabajador':
            self.load_workers_data()

    def load_workers_data(self, filters=None):
        """Carga los datos de los trabajadores en la tabla."""
        try:
            worker_data = self.db_manager.get_workers_summary(filters)
            self.table.setRowCount(len(worker_data))
            for row_idx, row_data in enumerate(worker_data):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los datos de los trabajadores:\n{e}")

    def closeEvent(self, event):
        """Asegura que la conexión de la BD se cierre al salir."""
        self.db_manager.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Es fundamental crear el DB Manager primero.
    db = DatabaseManager()

    # Mostrar la ventana de login
    login_dialog = LoginWindow(db)
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        # Si el login es exitoso, mostrar la ventana principal
        user_info = login_dialog.user_info
        main_win = MainWindow(db, user_info)
        main_win.show()
        sys.exit(app.exec())
    else:
        # Si el login falla o se cierra, salir de la aplicación
        db.close()
        sys.exit(0)
