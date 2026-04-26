from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from models import Usuario
from database import get_session

class LoginWindow(QWidget):

    login_exitoso = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario App")
        self.setFixedSize(400, 480)
        self.session = get_session()
        self._construir_ui()
        self._aplicar_estilos()

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        # Ícono
        icono = QLabel("🛒")
        icono.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icono.setStyleSheet("font-size: 48px; padding: 10px;")

        # Título
        titulo = QLabel("Inventario App")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #1E40AF;
        """)

        # Subtítulo
        subtitulo = QLabel("Gestión de descuentos dinámicos")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitulo.setStyleSheet("color: #6B7280; font-size: 13px;")

        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        separador.setStyleSheet("color: #E5E7EB; margin: 5px 0px;")

        # Usuario
        lbl_usuario = QLabel("Usuario")
        lbl_usuario.setStyleSheet("color: #374151; font-size: 13px; font-weight: bold;")
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ingresa tu usuario")
        self.input_usuario.setText("admin")
        self.input_usuario.setFixedHeight(40)

        # Contraseña
        lbl_password = QLabel("Contraseña")
        lbl_password.setStyleSheet("color: #374151; font-size: 13px; font-weight: bold;")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Ingresa tu contraseña")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setText("admin123")
        self.input_password.setFixedHeight(40)
        self.input_password.returnPressed.connect(self._iniciar_sesion)

        # Botón
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.setFixedHeight(44)
        self.btn_login.clicked.connect(self._iniciar_sesion)

        # Error
        self.lbl_error = QLabel("")
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_error.setStyleSheet("color: #DC2626; font-size: 12px;")

        # Footer
        footer = QLabel("v1.0.0")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #9CA3AF; font-size: 11px;")

        layout.addWidget(icono)
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addWidget(separador)
        layout.addWidget(lbl_usuario)
        layout.addWidget(self.input_usuario)
        layout.addWidget(lbl_password)
        layout.addWidget(self.input_password)
        layout.addSpacing(5)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.lbl_error)
        layout.addStretch()
        layout.addWidget(footer)

    def _iniciar_sesion(self):
        usuario_texto  = self.input_usuario.text().strip()
        password_texto = self.input_password.text().strip()

        if not usuario_texto or not password_texto:
            self.lbl_error.setText("⚠️ Completa todos los campos")
            return

        usuario = self.session.query(Usuario).filter(
            Usuario.usuario == usuario_texto,
            Usuario.activo  == 1
        ).first()

        if usuario and usuario.verificar_password(password_texto):
            self.lbl_error.setText("")
            self.login_exitoso.emit(usuario)
            self.close()
        else:
            self.lbl_error.setText("❌ Usuario o contraseña incorrectos")
            self.input_password.clear()

    def _aplicar_estilos(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F9FAFB;
                font-family: Segoe UI;
            }
            QLineEdit {
                background-color: #FFFFFF;
                color: #111827;
                border: 1.5px solid #D1D5DB;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1.5px solid #3B82F6;
            }
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton:pressed {
                background-color: #1E40AF;
            }
        """)