from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
from app.logic import registrar_trabajador

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
        ok, msg = registrar_trabajador(data)
        if ok:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", msg)
