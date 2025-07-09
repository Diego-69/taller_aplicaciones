import sys
import psycopg2
import bcrypt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel,
    QMessageBox, QDialog, QFormLayout, QComboBox, QStackedWidget,
    QGroupBox, QHeaderView
)
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QAction
from PyQt6.QtCore import Qt, pyqtSignal

# --- CONFIGURA TUS DATOS DE CONEXIÓN A POSTGRESQL AQUÍ ---
DB_CONFIG = {
    'dbname': 'taller_apps',
    'user': 'ignacio',
    'password': 'ignacio9980',
    'host': 'localhost',
    'port': '5432',
    'client_encoding': 'latin1' # Mantenemos esto por si hay caracteres especiales
}

class DatabaseManager:
    """
    Clase centralizada para manejar todas las interacciones con la base de datos.
    """
    def __init__(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
        except psycopg2.OperationalError as e:
            QMessageBox.critical(None, "Error de Conexión", f"No se pudo conectar a la base de datos:\n{e}")
            sys.exit(1)

    def check_user(self, username, password):
        """Verifica las credenciales del usuario."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT u.id, u.password_hash, u.rol_id, r.nombre, u.rut_trabajador
                FROM usuario u JOIN rol r ON u.rol_id = r.id
                WHERE u.username = %s AND u.activo = TRUE
            """, (username,))
            user_data = cur.fetchone()
            if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[1].encode('utf-8')):
                self.log_access(user_data[0], True)
                return {'id': user_data[0], 'role_id': user_data[2], 'role_name': user_data[3], 'worker_rut': user_data[4]}
            if user_data:
                self.log_access(user_data[0], False)
            return None

    def create_user(self, username, password, role_id, worker_rut=None):
        """Crea un nuevo usuario en la base de datos."""
        try:
            with self.conn.cursor() as cur:
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
                cur.execute("""
                    INSERT INTO usuario (username, password_hash, rol_id, rut_trabajador, activo)
                    VALUES (%s, %s, %s, %s, TRUE)
                """, (username, password_hash.decode('utf-8'), role_id, worker_rut))
                self.conn.commit()
            return True, "Usuario creado exitosamente."
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return False, "El nombre de usuario ya existe."
        except Exception as e:
            self.conn.rollback()
            return False, f"Ocurrió un error: {e}"

    def log_access(self, user_id, success):
        """Registra un intento de inicio de sesión."""
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO log_acceso (usuario_id, exito) VALUES (%s, %s)", (user_id, success))
            self.conn.commit()

    def get_workers_summary(self, filters=None):
        """Obtiene un listado resumen de los trabajadores."""
        query = "SELECT t.rut, t.nombre, t.sexo, dl.cargo FROM trabajador t JOIN datos_laborales dl ON t.rut = dl.rut_trabajador WHERE dl.estado = 'activo'"
        params = []
        if filters:
            conditions = []
            if filters.get('sexo'):
                conditions.append("t.sexo = %s")
                params.append(filters['sexo'])
            if filters.get('cargo'):
                conditions.append("dl.cargo ILIKE %s")
                params.append(f"%{filters['cargo']}%")
            if conditions:
                query += " AND " + " AND ".join(conditions)
        with self.conn.cursor() as cur:
            cur.execute(query, tuple(params))
            return cur.fetchall()

    def get_roles(self):
        """Obtiene todos los roles disponibles."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, nombre FROM rol ORDER BY nombre")
            return cur.fetchall()

    def get_unassigned_workers(self):
        """Obtiene trabajadores que aún no tienen una cuenta de usuario."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT t.rut, t.nombre FROM trabajador t
                LEFT JOIN usuario u ON t.rut = u.rut_trabajador
                WHERE u.rut_trabajador IS NULL AND t.rut IS NOT NULL
                ORDER BY t.nombre
            """)
            return cur.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()


class LoginAndRegisterWindow(QDialog):
    """
    Ventana unificada para iniciar sesión y registrar nuevos usuarios.
    """
    # Señal que se emite cuando el login es exitoso
    login_successful = pyqtSignal(dict)

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Bienvenido - El Correo de Yury")
        self.setFixedSize(400, 450)
        self.setStyleSheet("""
            QDialog { 
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #e8f4f8, stop: 1 #d1e9f2);
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel { 
                font-size: 14px; 
                color: #2c3e50;
                font-weight: 500;
            }
            QLabel[objectName="title"] {
                color: #1a365d;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QLineEdit { 
                padding: 12px 15px; 
                border: 2px solid #bdc3c7; 
                border-radius: 8px; 
                font-size: 14px;
                background-color: #ffffff;
                color: #2c3e50;
                selection-background-color: #3498db;
                min-height: 20px;
                line-height: 1.2;
            }
            QLineEdit::placeholder {
                color: #7f8c8d;
                font-style: italic;
            }
            QLineEdit:focus {
                border-color: #3498db;
                outline: none;
                box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
            }
            QComboBox {
                padding: 10px 15px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
                background-color: #ffffff;
                color: #2c3e50;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
                margin-right: 10px;
            }
            QPushButton { 
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #3498db, stop: 1 #2980b9);
                color: white; 
                padding: 12px 20px; 
                border-radius: 8px; 
                font-size: 16px; 
                font-weight: bold;
                border: none;
                min-height: 20px;
            }
            QPushButton:hover { 
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #2980b9, stop: 1 #21618c);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #21618c, stop: 1 #1b4f72);
            }
            QPushButton#linkButton {
                background: transparent; 
                color: #2980b9; 
                border: none;
                font-size: 13px; 
                text-decoration: underline; 
                font-weight: normal;
                padding: 8px;
            }
            QPushButton#linkButton:hover {
                color: #1a5490;
                background: rgba(52, 152, 219, 0.1);
                border-radius: 4px;
            }
        """)

        # Usamos un StackedWidget para cambiar entre login y registro
        self.stacked_widget = QStackedWidget()
        self.login_widget = self.create_login_widget()
        self.register_widget = self.create_register_widget()

        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.register_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)

    def create_login_widget(self):
        """Crea el widget de la interfaz de login."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("Iniciar Sesión")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))

        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("Nombre de usuario")
        self.login_pass = QLineEdit()
        self.login_pass.setPlaceholderText("Contraseña")
        self.login_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        login_button = QPushButton("Ingresar")
        login_button.clicked.connect(self.handle_login)

        register_link = QPushButton("¿No tienes cuenta? Regístrate aquí")
        register_link.setObjectName("linkButton")
        register_link.setCursor(Qt.CursorShape.PointingHandCursor)
        register_link.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        layout.addWidget(title)
        layout.addWidget(self.login_user)
        layout.addWidget(self.login_pass)
        layout.addWidget(login_button)
        layout.addStretch()
        layout.addWidget(register_link, alignment=Qt.AlignmentFlag.AlignCenter)
        return widget

    def create_register_widget(self):
        """Crea el widget de la interfaz de registro."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("Crear Nueva Cuenta")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))

        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("Nombre de usuario")
        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("Contraseña")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass_confirm = QLineEdit()
        self.reg_pass_confirm.setPlaceholderText("Confirmar contraseña")
        self.reg_pass_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.reg_role = QComboBox()
        self.reg_role.addItem("-- Seleccione un rol --", None)
        for role_id, role_name in self.db_manager.get_roles():
            self.reg_role.addItem(role_name.capitalize(), role_id)
        
        # El ComboBox para trabajadores, inicialmente oculto
        self.worker_label = QLabel("Asociar a Trabajador:")
        self.reg_worker = QComboBox()
        self.worker_label.hide()
        self.reg_worker.hide()
        self.reg_role.currentTextChanged.connect(self.toggle_worker_selection)

        register_button = QPushButton("Registrar")
        register_button.clicked.connect(self.handle_register)

        back_link = QPushButton("Volver a Inicio de Sesión")
        back_link.setObjectName("linkButton")
        back_link.setCursor(Qt.CursorShape.PointingHandCursor)
        back_link.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        layout.addWidget(title)
        layout.addWidget(self.reg_user)
        layout.addWidget(self.reg_pass)
        layout.addWidget(self.reg_pass_confirm)
        layout.addWidget(QLabel("Rol de Usuario:"))
        layout.addWidget(self.reg_role)
        layout.addWidget(self.worker_label)
        layout.addWidget(self.reg_worker)
        layout.addWidget(register_button)
        layout.addStretch()
        layout.addWidget(back_link, alignment=Qt.AlignmentFlag.AlignCenter)
        return widget
        
    def toggle_worker_selection(self, role_name):
        """Muestra u oculta el selector de trabajador basado en el rol."""
        if role_name.lower() == 'trabajador':
            self.reg_worker.clear()
            self.reg_worker.addItem("-- Seleccione un trabajador --", None)
            for rut, nombre in self.db_manager.get_unassigned_workers():
                self.reg_worker.addItem(f"{nombre} ({rut})", rut)
            self.worker_label.show()
            self.reg_worker.show()
        else:
            self.worker_label.hide()
            self.reg_worker.hide()

    def handle_login(self):
        user = self.login_user.text()
        password = self.login_pass.text()
        if not user or not password:
            QMessageBox.warning(self, "Datos incompletos", "Debe ingresar usuario y contraseña.")
            return
        
        user_info = self.db_manager.check_user(user, password)
        if user_info:
            self.login_successful.emit(user_info) # Emitir señal con los datos del usuario
            self.accept() # Cerrar el diálogo de login
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")

    def handle_register(self):
        user = self.reg_user.text()
        password = self.reg_pass.text()
        confirm_pass = self.reg_pass_confirm.text()
        role_id = self.reg_role.currentData()
        
        if not all([user, password, confirm_pass, role_id is not None]):
            QMessageBox.warning(self, "Datos incompletos", "Todos los campos son obligatorios.")
            return
        if password != confirm_pass:
            QMessageBox.warning(self, "Error de Contraseña", "Las contraseñas no coinciden.")
            return
            
        worker_rut = None
        if self.reg_role.currentText().lower() == 'trabajador':
            worker_rut = self.reg_worker.currentData()
            if worker_rut is None:
                QMessageBox.warning(self, "Datos incompletos", "Debe seleccionar un trabajador para asociar la cuenta.")
                return

        success, message = self.db_manager.create_user(user, password, role_id, worker_rut)
        if success:
            QMessageBox.information(self, "Éxito", message)
            self.login_user.setText(user) # Pre-rellenar el campo de usuario en el login
            self.login_pass.clear()
            self.stacked_widget.setCurrentIndex(0) # Volver al login
        else:
            QMessageBox.critical(self, "Error de Registro", message)


class MainWindow(QMainWindow):
    """
    Ventana Principal de la aplicación, visible después del login.
    """
    logout_requested = pyqtSignal()

    def __init__(self, user_info, db_manager):
        super().__init__()
        self.user_info = user_info
        self.db_manager = db_manager
        self.initUI()
        self.load_initial_data()

    def initUI(self):
        self.setWindowTitle(f"SIGERH - El Correo de Yury (Usuario: {self.user_info['role_name'].capitalize()})")
        self.setGeometry(100, 100, 1200, 700)
        
        # Menú
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&Archivo")
        logout_action = QAction("Cerrar Sesión", self)
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)

        # La interfaz se adapta al rol del usuario
        if self.user_info['role_name'] in ['admin', 'jefe_rrhh', 'rrhh']:
            self.setup_hr_ui()
        elif self.user_info['role_name'] == 'trabajador':
            self.setup_worker_ui()

    def setup_hr_ui(self):
        """Configura la interfaz para usuarios de RR.HH."""
        # Panel izquierdo con filtros y acciones
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(300)

        # Filtros (solo para jefe_rrhh)
        filter_group = QGroupBox("Filtros de Búsqueda")
        filter_layout = QFormLayout()
        self.sexo_filter = QComboBox()
        self.sexo_filter.addItems(["Todos", "Masculino", "Femenino"])
        self.cargo_filter = QLineEdit()
        filter_layout.addRow("Sexo:", self.sexo_filter)
        filter_layout.addRow("Cargo:", self.cargo_filter)
        filter_group.setLayout(filter_layout)
        
        self.filter_button = QPushButton("Filtrar")
        self.clear_button = QPushButton("Limpiar Filtros")
        self.filter_button.clicked.connect(self.apply_filters)
        self.clear_button.clicked.connect(self.clear_filters)

        # Acciones
        action_group = QGroupBox("Acciones")
        action_layout = QVBoxLayout()
        self.add_button = QPushButton("Agregar Trabajador")
        self.edit_button = QPushButton("Ver/Editar Ficha")
        self.delete_button = QPushButton("Dar de Baja")
        action_layout.addWidget(self.add_button)
        action_layout.addWidget(self.edit_button)
        action_layout.addWidget(self.delete_button)
        action_group.setLayout(action_layout)

        left_layout.addWidget(filter_group)
        left_layout.addWidget(self.filter_button)
        left_layout.addWidget(self.clear_button)
        left_layout.addWidget(action_group)
        left_layout.addStretch()
        
        # Ocultar filtros si no es jefe de rrhh
        is_jefe = self.user_info['role_name'] == 'jefe_rrhh'
        filter_group.setVisible(is_jefe)
        self.filter_button.setVisible(is_jefe)
        self.clear_button.setVisible(is_jefe)

        # Panel derecho con la tabla
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["RUT", "Nombre", "Sexo", "Cargo"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.main_layout.addWidget(left_panel)
        self.main_layout.addWidget(self.table)

    def setup_worker_ui(self):
        """Configura la interfaz para un trabajador."""
        # ... (La lógica para la vista del trabajador iría aquí)
        label = QLabel(f"Bienvenido, trabajador {self.user_info['worker_rut']}.\n\nVista de empleado en construcción.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Arial", 18))
        self.main_layout.addWidget(label)

    def load_initial_data(self):
        if self.user_info['role_name'] != 'trabajador':
            self.load_workers_data()

    def load_workers_data(self, filters=None):
        try:
            worker_data = self.db_manager.get_workers_summary(filters)
            self.table.setRowCount(len(worker_data))
            for row_idx, row_data in enumerate(worker_data):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los datos: {e}")

    def apply_filters(self):
        filters = {}
        if self.sexo_filter.currentIndex() > 0:
            filters['sexo'] = self.sexo_filter.currentText()
        if self.cargo_filter.text():
            filters['cargo'] = self.cargo_filter.text()
        self.load_workers_data(filters)

    def clear_filters(self):
        self.sexo_filter.setCurrentIndex(0)
        self.cargo_filter.clear()
        self.load_workers_data()
        
    def logout(self):
        self.logout_requested.emit()
        self.close()

def main():
    """Función principal que controla el flujo de la aplicación."""
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()
    
    # Bucle para manejar el login/logout
    while True:
        login_window = LoginAndRegisterWindow(db_manager)
        
        # Variable para guardar los datos del usuario si el login es exitoso
        user_info = None
        
        def on_login_success(info):
            nonlocal user_info
            user_info = info
        
        login_window.login_successful.connect(on_login_success)
        
        # Muestra la ventana de login y espera a que se cierre
        login_window.exec()
        
        if user_info:
            main_window = MainWindow(user_info, db_manager)
            
            # Variable para saber si se solicitó logout
            logout_flag = False
            def handle_logout():
                nonlocal logout_flag
                logout_flag = True

            main_window.logout_requested.connect(handle_logout)
            main_window.show()
            app.exec() # Inicia el bucle de eventos de la ventana principal
            
            # Si el bucle termina y logout_flag es True, el while continuará
            # para mostrar de nuevo la ventana de login.
            if not logout_flag:
                break # Si se cierra la ventana principal sin logout, termina la app
        else:
            # Si se cierra la ventana de login sin éxito, termina la app
            break

    db_manager.close()
    sys.exit()


if __name__ == '__main__':
    main()