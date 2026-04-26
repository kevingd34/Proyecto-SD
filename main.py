import sys
from PyQt6.QtWidgets import QApplication
from database import inicializar_bd
from ui.login import LoginWindow
from ui.main_window import MainWindow

def main():
    inicializar_bd()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    def abrir_sistema(usuario):
        global ventana
        ventana = MainWindow(usuario)
        ventana.show()

    login = LoginWindow()
    login.login_exitoso.connect(abrir_sistema)
    login.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()