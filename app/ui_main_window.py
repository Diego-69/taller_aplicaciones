"""
Ventana principal de la aplicación El Correo de Yury.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox
from app.database import get_all_workers, delete_worker, get_cargas_by_trabajador, get_contactos_by_trabajador
from app.database import insert_carga, update_carga, delete_carga, insert_contacto, update_contacto, delete_contacto
from app.database import get_all_cargos, get_all_departamentos
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
        # Botón cerrar sesión siempre visible
        logout_btn = QPushButton("Cerrar sesión")
        logout_btn.clicked.connect(self.logout)
        action_layout.addWidget(logout_btn)
        self.layout.addLayout(action_layout)

        if self.perfil == 'RRHH':
            add_btn = QPushButton("Añadir Trabajador")
            add_btn.clicked.connect(self.add_worker)
            action_layout.insertWidget(0, add_btn)
            del_btn = QPushButton("Eliminar Trabajador(es)")
            del_btn.clicked.connect(self.delete_workers)
            action_layout.insertWidget(1, del_btn)
            self.table = QTableWidget()
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["RUT", "Nombre", "Sexo", "Cargo", "Acciones"])
            self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)
            self.layout.addWidget(self.table)
            self.load_workers()
        elif self.perfil == 'Trabajador':
            # Mostrar solo datos del trabajador logueado
            from app.database import get_worker_by_rut, get_cargas_by_trabajador, get_contactos_by_trabajador
            datos = get_worker_by_rut(self.rut_trabajador)
            if datos:
                info = QLabel(f"<b>Bienvenido, {datos[1]}</b><br>RUT: {datos[0]}<br>Sexo: {datos[2]}<br>Dirección: {datos[3]}<br>Teléfono: {datos[4]}<br>Cargo: {datos[7]}<br>Departamento: {datos[8]}")
                self.layout.addWidget(info)
            else:
                self.layout.addWidget(QLabel("No se encontraron datos personales."))

            # Panel de cargas familiares
            cargas = get_cargas_by_trabajador(self.rut_trabajador)
            cargas_label = QLabel("<b>Cargas Familiares:</b>")
            self.layout.addWidget(cargas_label)
            if cargas:
                cargas_table = QTableWidget()
                cargas_table.setColumnCount(4)
                cargas_table.setHorizontalHeaderLabels(["RUT", "Nombre", "Parentesco", "Sexo"])
                cargas_table.setRowCount(len(cargas))
                for row_idx, carga in enumerate(cargas):
                    for col_idx, value in enumerate(carga[1:]):
                        cargas_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
                cargas_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                self.layout.addWidget(cargas_table)
            else:
                self.layout.addWidget(QLabel("No tienes cargas familiares registradas."))

            # Panel de contactos de emergencia
            contactos = get_contactos_by_trabajador(self.rut_trabajador)
            contactos_label = QLabel("<b>Contactos de Emergencia:</b>")
            self.layout.addWidget(contactos_label)
            if contactos:
                contactos_table = QTableWidget()
                contactos_table.setColumnCount(3)
                contactos_table.setHorizontalHeaderLabels(["Nombre", "Relación", "Teléfono"])
                contactos_table.setRowCount(len(contactos))
                for row_idx, contacto in enumerate(contactos):
                    for col_idx, value in enumerate(contacto[1:]):
                        contactos_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
                contactos_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
                self.layout.addWidget(contactos_table)
            else:
                self.layout.addWidget(QLabel("No tienes contactos de emergencia registrados."))
        else:
            self.layout.addWidget(QLabel("Perfil no soportado."))

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
        dlg = WorkerFormDialog(self)
        if dlg.exec():
            self.load_workers()

    def delete_workers(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Selecciona", "Selecciona uno o más trabajadores para eliminar.")
            return
        ruts = [self.table.item(idx.row(), 0).text() for idx in selected]
        ok = QMessageBox.question(self, "Confirmar", f"¿Eliminar los siguientes trabajadores?\n{chr(10).join(ruts)}")
        if ok:
            errores = []
            for rut in ruts:
                success, msg = delete_worker(rut)
                if not success:
                    errores.append(f"{rut}: {msg}")
            if not errores:
                QMessageBox.information(self, "Eliminado", "Todos los trabajadores seleccionados fueron eliminados.")
            else:
                QMessageBox.warning(self, "Algunos no eliminados", "No se pudieron eliminar:\n" + "\n".join(errores))
            self.load_workers()

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
        self.rut_trabajador = rut_trabajador
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
        cargas = get_cargas_by_trabajador(self.rut_trabajador)
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
            success, msg = insert_carga([rut, self.rut_trabajador, nombre, parentesco, sexo])
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
        self.rut_trabajador = rut_trabajador
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
        contactos = get_contactos_by_trabajador(self.rut_trabajador)
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
            success, msg = insert_contacto([self.rut_trabajador, nombre, relacion, telefono])
        if success:
            QMessageBox.information(self, "Éxito", msg)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", msg)

class WorkerFormDialog(QDialog):
    """
    Formulario para añadir un nuevo trabajador desde RRHH.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Añadir Trabajador")
        layout = QFormLayout()
        self.rut_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.sexo_combo = QComboBox()
        self.sexo_combo.addItems(["Masculino", "Femenino", "Otro"])
        self.direccion_input = QLineEdit()
        self.telefono_input = QLineEdit()
        
        self.cargo_combo = QComboBox()
        self.depto_combo = QComboBox()
        self.load_combos()

        layout.addRow("RUT:", self.rut_input)
        layout.addRow("Nombre completo:", self.nombre_input)
        layout.addRow("Sexo:", self.sexo_combo)
        layout.addRow("Dirección:", self.direccion_input)
        layout.addRow("Teléfono:", self.telefono_input)
        layout.addRow("Cargo:", self.cargo_combo)
        layout.addRow("Departamento:", self.depto_combo)
        
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save)
        layout.addRow(save_btn)
        self.setLayout(layout)

    def load_combos(self):
        self.cargos = get_all_cargos()
        self.deptos = get_all_departamentos()
        for cargo_id, nombre_cargo in self.cargos:
            self.cargo_combo.addItem(nombre_cargo, cargo_id)
        for depto_id, nombre_depto in self.deptos:
            self.depto_combo.addItem(nombre_depto, depto_id)

    def save(self):
        from app.database import insert_worker
        rut = self.rut_input.text().strip()
        nombre = self.nombre_input.text().strip()
        sexo = self.sexo_combo.currentText()
        direccion = self.direccion_input.text().strip()
        telefono = self.telefono_input.text().strip()
        
        id_cargo = self.cargo_combo.currentData()
        id_depto = self.depto_combo.currentData()

        if not all([rut, nombre, sexo, id_cargo, id_depto]):
            QMessageBox.warning(self, "Datos incompletos", "Todos los campos obligatorios (RUT, Nombre, Sexo, Cargo, Departamento) deben estar completos.")
            return
        if not validar_rut(rut):
            QMessageBox.warning(self, "RUT inválido", "El RUT ingresado no tiene un formato válido.")
            return
        if telefono and not validar_telefono(telefono):
            QMessageBox.warning(self, "Teléfono inválido", "El teléfono debe contener solo números y opcionalmente '+'.")
            return
            
        # La fecha de ingreso se puede manejar automáticamente en la BD o aquí
        from datetime import date
        fecha_ingreso = date.today().isoformat()

        ok, msg = insert_worker((rut, nombre, sexo, direccion, telefono, fecha_ingreso, id_cargo, id_depto))
        if ok:
            QMessageBox.information(self, "Éxito", msg)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", msg)
