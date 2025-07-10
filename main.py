import sys
from PyQt6.QtWidgets import QApplication
from app.ui_login import LoginWindow
from app.ui_main_window import MainWindow

class AppController:
    """
    Controlador principal de la aplicación.
    Gestiona la transición entre login y ventana principal.
    """
    def __init__(self):
        self.app = QApplication(sys.argv)
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