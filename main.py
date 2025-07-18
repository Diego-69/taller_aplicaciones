import sys
from PyQt6.QtWidgets import QApplication
from app.ui_login import LoginWindow
from app.ui_main_window import MainWindow

APP_STYLE = """
QWidget {
    background: #f4f6fa;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 15px;
}
QLabel {
    color: #222;
    font-size: 15px;
}
QPushButton {
    background-color: #4f8cff;
    color: white;
    border-radius: 8px;
    padding: 6px 16px;
    font-weight: bold;
    font-size: 15px;
}
QPushButton:hover {
    background-color: #357ae8;
}
QLineEdit, QComboBox {
    background: #fff;
    border: 1px solid #bfc7d5;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 15px;
}
QTableWidget {
    background: #fff;
    border-radius: 8px;
    font-size: 15px;
    gridline-color: #e0e6ed;
}
QHeaderView::section {
    background: #e0e6ed;
    color: #222;
    font-weight: bold;
    border-radius: 6px;
    padding: 4px;
}
QDialog {
    background: #f4f6fa;
    border-radius: 12px;
}
"""

class AppController:
    """
    Controlador principal de la aplicación.
    Gestiona la transición entre login y ventana principal.
    """
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(APP_STYLE)
        self.login_window = None
        self.main_window = None

    def show_login(self):
        self.login_window = LoginWindow(main_app=self)
        self.login_window.show()

    def show_main_window(self, perfil, rut_trabajador):
        self.main_window = MainWindow(perfil, rut_trabajador, main_app=self)
        self.main_window.show()
        self.main_window.destroyed.connect(self.show_login)

    def run(self):
        self.show_login()
        sys.exit(self.app.exec())

def main():
    controller = AppController()
    controller.run()

if __name__ == '__main__':
    main()