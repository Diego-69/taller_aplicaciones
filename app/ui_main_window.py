"""
Ventana principal de la aplicación El Correo de Yury.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox
from app.database import get_all_workers, delete_worker, get_cargas_by_trabajador, get_contactos_by_trabajador
from app.database import insert_carga, update_carga, delete_carga, insert_contacto, update_contacto, delete_contacto
import re

def validar_rut(rut: str) -> bool:
    """Valida el formato básico de un RUT chileno."""
    return bool(re.match(r'^[0-9]{7,8}-[0-9kK]$', rut))

def validar_telefono(telefono: str) -> bool:
    """Valida que el teléfono contenga solo números y opcionalmente +."""
    return bool(re.match(r'^\+?[0-9]{8,15}$', telefono))

class MainWindow(QWidget):
    """
    Ventana principal de la aplicación.
    Permite a RRHH gestionar trabajadores, cargas familiares y contactos de emergencia.
    :param perfil: Perfil del usuario.
    :param rut_trabajador: RUT del trabajador (si aplica).
    :param main_app: Referencia al controlador principal para cerrar sesión.
    """
    def __init__(self, perfil, rut_trabajador=None, main_app=None):
        super().__init__()
        self.perfil = perfil
        self.rut_trabajador = rut_trabajador
        self.main_app = main_app
        self.setWindowTitle(f"El Correo de Yury - Perfil: {self.perfil}")
        self.setGeometry(100, 100, 900, 600)
        self.layout = QVBoxLayout()
        self.setup_ui()
        self.setLayout(self.layout)

    def setup_ui(self):
        action_layout = QHBoxLayout()
        if self.perfil == 'RRHH':
            add_btn = QPushButton("Añadir Trabajador")
            add_btn.clicked.connect(self.add_worker)
            action_layout.addWidget(add_btn)
            del_btn = QPushButton("Eliminar Trabajador")
            del_btn.clicked.connect(self.delete_worker)
            action_layout.addWidget(del_btn)
        # Botón cerrar sesión
        logout_btn = QPushButton("Cerrar sesión")
        logout_btn.clicked.connect(self.logout)
        action_layout.addWidget(logout_btn)
        self.layout.addLayout(action_layout)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["RUT", "Nombre", "Sexo", "Cargo", "Acciones"])
        self.layout.addWidget(self.table)
        self.load_workers()

    def logout(self):
        self.close()
        if self.main_app:
            self.main_app.show_login()

    def load_workers(self):
        self.table.setRowCount(0)
        workers = get_all_workers()
        for row_idx, worker in enumerate(workers):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(worker[:4]):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
            # Botón de acciones
            btn = QPushButton("Ver Detalle")
            btn.clicked.connect(lambda _, rut=worker[0]: self.open_worker_detail(rut))
            self.table.setCellWidget(row_idx, 4, btn)

    def add_worker(self):
        QMessageBox.information(self, "Función", "Aquí se abriría el formulario para añadir trabajador.")
        # Aquí se llamaría a un diálogo de alta y luego self.load_workers()

    def delete_worker(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selecciona", "Selecciona un trabajador para eliminar.")
            return
        rut = self.table.item(row, 0).text()
        ok = QMessageBox.question(self, "Confirmar", f"¿Eliminar trabajador {rut}?")
        if ok:
            success, msg = delete_worker(rut)
            if success:
                QMessageBox.information(self, "Eliminado", msg)
                self.load_workers()
            else:
                QMessageBox.critical(self, "Error", msg)

    def open_worker_detail(self, rut):
        dlg = WorkerDetailDialog(rut)
        dlg.exec()
        self.load_workers()

class WorkerDetailDialog(QDialog):
    """
    Diálogo para ver y gestionar cargas familiares y contactos de emergencia de un trabajador.
    """
    def __init__(self, rut_trabajador):
        super().__init__()
        self.rut_trabajador = rut_trabajador
        self.setWindowTitle(f"Detalle de {rut_trabajador}")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"RUT: {rut_trabajador}"))
        # Botones para gestionar cargas/contactos
        btns = QHBoxLayout()
        btn_cargas = QPushButton("Gestionar Cargas Familiares")
        btn_cargas.clicked.connect(self.open_cargas_dialog)
        btns.addWidget(btn_cargas)
        btn_contactos = QPushButton("Gestionar Contactos de Emergencia")
        btn_contactos.clicked.connect(self.open_contactos_dialog)
        btns.addWidget(btn_contactos)
        layout.addLayout(btns)
        self.setLayout(layout)

    def open_cargas_dialog(self):
        dlg = CargasDialog(self.rut_trabajador)
        dlg.exec()

    def open_contactos_dialog(self):
        dlg = ContactosDialog(self.rut_trabajador)
        dlg.exec()

class CargasDialog(QDialog):
    """
    Diálogo para CRUD de cargas familiares.
    """
    def __init__(self, rut_trabajador):
        super().__init__()
        self.rut_trabajador = rut_trabajador
        self.setWindowTitle("Cargas Familiares")
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["RUT", "Nombre", "Parentesco", "Sexo"])
        layout.addWidget(self.table)
        btns = QHBoxLayout()
        add_btn = QPushButton("Añadir")
        add_btn.clicked.connect(self.add_carga)
        btns.addWidget(add_btn)
        edit_btn = QPushButton("Editar")
        edit_btn.clicked.connect(self.edit_carga)
        btns.addWidget(edit_btn)
        del_btn = QPushButton("Eliminar")
        del_btn.clicked.connect(self.delete_carga)
        btns.addWidget(del_btn)
        layout.addLayout(btns)
        self.setLayout(layout)
        self.load_cargas()

    def load_cargas(self):
        cargas = get_cargas_by_trabajador(self.rut_trabajador)
        self.table.setRowCount(0)
        for row_idx, carga in enumerate(cargas):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(carga[1:]):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_carga(self):
        dlg = CargaFormDialog(self.rut_trabajador)
        if dlg.exec():
            self.load_cargas()

    def edit_carga(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selecciona", "Selecciona una carga para editar.")
            return
        id_carga = get_cargas_by_trabajador(self.rut_trabajador)[row][0]
        dlg = CargaFormDialog(self.rut_trabajador, id_carga)
        if dlg.exec():
            self.load_cargas()

    def delete_carga(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selecciona", "Selecciona una carga para eliminar.")
            return
        id_carga = get_cargas_by_trabajador(self.rut_trabajador)[row][0]
        ok = QMessageBox.question(self, "Confirmar", "¿Eliminar carga?")
        if ok:
            success, msg = delete_carga(id_carga)
            if success:
                QMessageBox.information(self, "Eliminado", msg)
                self.load_cargas()
            else:
                QMessageBox.critical(self, "Error", msg)

class CargaFormDialog(QDialog):
    """
    Formulario para añadir o editar una carga familiar.
    Valida campos obligatorios y formato de RUT.
    """
    def __init__(self, rut_trabajador, id_carga=None):
        super().__init__()
        self.id_carga = id_carga
        self.setWindowTitle("Carga Familiar")
        layout = QFormLayout()
        self.rut_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.parentesco_input = QLineEdit()
        self.sexo_combo = QComboBox()
        self.sexo_combo.addItems(["Masculino", "Femenino", "Otro"])
        layout.addRow("RUT:", self.rut_input)
        layout.addRow("Nombre:", self.nombre_input)
        layout.addRow("Parentesco:", self.parentesco_input)
        layout.addRow("Sexo:", self.sexo_combo)
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save)
        layout.addRow(save_btn)
        self.setLayout(layout)
        if id_carga:
            self.load_data()

    def load_data(self):
        cargas = get_cargas_by_trabajador(self.parent().rut_trabajador)
        for carga in cargas:
            if carga[0] == self.id_carga:
                self.rut_input.setText(carga[1])
                self.nombre_input.setText(carga[2])
                self.parentesco_input.setText(carga[3])
                self.sexo_combo.setCurrentText(carga[4])

    def save(self):
        rut = self.rut_input.text().strip()
        nombre = self.nombre_input.text().strip()
        parentesco = self.parentesco_input.text().strip()
        sexo = self.sexo_combo.currentText()
        if not all([rut, nombre, parentesco, sexo]):
            QMessageBox.warning(self, "Datos incompletos", "Todos los campos son obligatorios.")
            return
        if not validar_rut(rut):
            QMessageBox.warning(self, "RUT inválido", "El RUT ingresado no tiene un formato válido.")
            return
        if self.id_carga:
            success, msg = update_carga(self.id_carga, [rut, nombre, parentesco, sexo])
        else:
            success, msg = insert_carga([rut, self.parent().rut_trabajador, nombre, parentesco, sexo])
        if success:
            QMessageBox.information(self, "Éxito", msg)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", msg)

class ContactosDialog(QDialog):
    """
    Diálogo para CRUD de contactos de emergencia.
    """
    def __init__(self, rut_trabajador):
        super().__init__()
        self.rut_trabajador = rut_trabajador
        self.setWindowTitle("Contactos de Emergencia")
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nombre", "Relación", "Teléfono"])
        layout.addWidget(self.table)
        btns = QHBoxLayout()
        add_btn = QPushButton("Añadir")
        add_btn.clicked.connect(self.add_contacto)
        btns.addWidget(add_btn)
        edit_btn = QPushButton("Editar")
        edit_btn.clicked.connect(self.edit_contacto)
        btns.addWidget(edit_btn)
        del_btn = QPushButton("Eliminar")
        del_btn.clicked.connect(self.delete_contacto)
        btns.addWidget(del_btn)
        layout.addLayout(btns)
        self.setLayout(layout)
        self.load_contactos()

    def load_contactos(self):
        contactos = get_contactos_by_trabajador(self.rut_trabajador)
        self.table.setRowCount(0)
        for row_idx, contacto in enumerate(contactos):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(contacto[1:]):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_contacto(self):
        dlg = ContactoFormDialog(self.rut_trabajador)
        if dlg.exec():
            self.load_contactos()

    def edit_contacto(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selecciona", "Selecciona un contacto para editar.")
            return
        id_contacto = get_contactos_by_trabajador(self.rut_trabajador)[row][0]
        dlg = ContactoFormDialog(self.rut_trabajador, id_contacto)
        if dlg.exec():
            self.load_contactos()

    def delete_contacto(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selecciona", "Selecciona un contacto para eliminar.")
            return
        id_contacto = get_contactos_by_trabajador(self.rut_trabajador)[row][0]
        ok = QMessageBox.question(self, "Confirmar", "¿Eliminar contacto?")
        if ok:
            success, msg = delete_contacto(id_contacto)
            if success:
                QMessageBox.information(self, "Eliminado", msg)
                self.load_contactos()
            else:
                QMessageBox.critical(self, "Error", msg)

class ContactoFormDialog(QDialog):
    """
    Formulario para añadir o editar un contacto de emergencia.
    Valida campos obligatorios y formato de teléfono.
    """
    def __init__(self, rut_trabajador, id_contacto=None):
        super().__init__()
        self.id_contacto = id_contacto
        self.setWindowTitle("Contacto de Emergencia")
        layout = QFormLayout()
        self.nombre_input = QLineEdit()
        self.relacion_input = QLineEdit()
        self.telefono_input = QLineEdit()
        layout.addRow("Nombre:", self.nombre_input)
        layout.addRow("Relación:", self.relacion_input)
        layout.addRow("Teléfono:", self.telefono_input)
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save)
        layout.addRow(save_btn)
        self.setLayout(layout)
        if id_contacto:
            self.load_data()

    def load_data(self):
        contactos = get_contactos_by_trabajador(self.parent().rut_trabajador)
        for contacto in contactos:
            if contacto[0] == self.id_contacto:
                self.nombre_input.setText(contacto[1])
                self.relacion_input.setText(contacto[2])
                self.telefono_input.setText(contacto[3])

    def save(self):
        nombre = self.nombre_input.text().strip()
        relacion = self.relacion_input.text().strip()
        telefono = self.telefono_input.text().strip()
        if not all([nombre, relacion, telefono]):
            QMessageBox.warning(self, "Datos incompletos", "Todos los campos son obligatorios.")
            return
        if not validar_telefono(telefono):
            QMessageBox.warning(self, "Teléfono inválido", "El teléfono debe contener solo números y opcionalmente '+'.")
            return
        if self.id_contacto:
            success, msg = update_contacto(self.id_contacto, [nombre, relacion, telefono])
        else:
            success, msg = insert_contacto([self.parent().rut_trabajador, nombre, relacion, telefono])
        if success:
            QMessageBox.information(self, "Éxito", msg)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", msg)
