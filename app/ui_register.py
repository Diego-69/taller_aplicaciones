from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
from app.logic import registrar_trabajador
import re

def validar_rut(rut: str) -> bool:
    return bool(re.match(r'^[0-9]{7,8}-[0-9kK]$', rut))

def validar_telefono(telefono: str) -> bool:
    return bool(re.match(r'^\+?[0-9]{8,15}$', telefono))

class RegisterDialog(QDialog):
    """
    Diálogo para registrar un nuevo usuario con perfil Trabajador.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registro de Trabajador")
        layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.rut_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.sexo_combo = QComboBox()
        self.sexo_combo.addItems(["Masculino", "Femenino", "Otro"])
        self.direccion_input = QLineEdit()
        self.telefono_input = QLineEdit()
        layout.addRow("Usuario:", self.username_input)
        layout.addRow("Contraseña:", self.password_input)
        layout.addRow("RUT:", self.rut_input)
        layout.addRow("Nombre completo:", self.nombre_input)
        layout.addRow("Sexo:", self.sexo_combo)
        layout.addRow("Dirección:", self.direccion_input)
        layout.addRow("Teléfono:", self.telefono_input)
        btn = QPushButton("Registrar")
        btn.clicked.connect(self.handle_register)
        layout.addRow(btn)
        self.setLayout(layout)

    def handle_register(self):
        data = {
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip(),
            "rut": self.rut_input.text().strip(),
            "nombre": self.nombre_input.text().strip(),
            "sexo": self.sexo_combo.currentText(),
            "direccion": self.direccion_input.text().strip(),
            "telefono": self.telefono_input.text().strip(),
        }
        # Validaciones detalladas
        if not all([data["username"], data["password"], data["rut"], data["nombre"], data["sexo"]]):
            QMessageBox.warning(self, "Datos incompletos", "Todos los campos obligatorios deben estar completos.")
            return
        if len(data["username"]) < 4:
            QMessageBox.warning(self, "Usuario muy corto", "El nombre de usuario debe tener al menos 4 caracteres.")
            return
        if len(data["password"]) < 6:
            QMessageBox.warning(self, "Contraseña muy corta", "La contraseña debe tener al menos 6 caracteres.")
            return
        if not validar_rut(data["rut"]):
            QMessageBox.warning(self, "RUT inválido", "El RUT ingresado no tiene un formato válido.")
            return
        if data["telefono"] and not validar_telefono(data["telefono"]):
            QMessageBox.warning(self, "Teléfono inválido", "El teléfono debe contener solo números y opcionalmente '+'.")
            return
        ok, msg = registrar_trabajador(data)
        if ok:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", msg)
