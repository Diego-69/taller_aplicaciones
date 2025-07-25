"""
Ventana de Login para El Correo de Yury.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from app.logic import autenticar_usuario
from app.ui_register import RegisterDialog

class LoginWindow(QWidget):
    """
    Ventana de login. Permite al usuario iniciar sesión.
    """
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("Login - El Correo de Yury")
        self.setGeometry(100, 100, 300, 150)
        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        layout.addWidget(self.username_input)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        login_button = QPushButton("Iniciar Sesión")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)
        self.setLayout(layout)
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        perfil, rut_trabajador = autenticar_usuario(username, password)
        if perfil:
            self.main_app.show_main_window(perfil, rut_trabajador)
            self.close()
        else:
            QMessageBox.warning(self, "Login Fallido", "Usuario o contraseña incorrectos.")
    def open_register(self):
        dlg = RegisterDialog(self)
        if dlg.exec():
            QMessageBox.information(self, "Registro exitoso", "¡Usuario registrado! Ahora puede iniciar sesión.")
