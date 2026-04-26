from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from risk_engine import RiskEngine

class MainWindow(QMainWindow):

    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Inventario App")
        self.setMinimumSize(1100, 700)
        self.engine = RiskEngine()

        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QHBoxLayout(central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        self.sidebar   = self._crear_sidebar()
        self.contenido = QStackedWidget()
        self.contenido.setStyleSheet("background-color: #F3F4F6;")

        layout_principal.addWidget(self.sidebar)
        layout_principal.addWidget(self.contenido)

        self._cargar_vistas()
        self._aplicar_estilos()

        self.timer = QTimer()
        self.timer.timeout.connect(self._escanear_automatico)
        self.timer.start(60000)
        self._escanear_automatico()

    def _crear_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setFixedWidth(210)
        sidebar.setObjectName("sidebar")

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Encabezado
        header = QFrame()
        header.setObjectName("sidebar_header")
        header.setFixedHeight(80)
        header_layout = QVBoxLayout(header)
        titulo = QLabel("🛒  Inventario App")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setObjectName("sidebar_titulo")
        header_layout.addWidget(titulo)
        layout.addWidget(header)

        # Usuario
        usuario_lbl = QLabel(f"👤  {self.usuario.nombre}")
        usuario_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        usuario_lbl.setObjectName("usuario_lbl")
        usuario_lbl.setFixedHeight(35)
        layout.addWidget(usuario_lbl)

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #E5E7EB; margin: 0px 15px;")
        layout.addWidget(sep)
        layout.addSpacing(8)

        # Navegación
        self.botones_nav = []
        opciones = [
            ("📊   Dashboard",      0),
            ("📦   Inventario",     1),
            ("🚨   Alertas",        2),
            ("⚙️    Configuración", 3),
        ]

        for texto, index in opciones:
            btn = QPushButton(texto)
            btn.setObjectName("nav_btn")
            btn.setFixedHeight(46)
            btn.clicked.connect(lambda checked, i=index: self._cambiar_vista(i))
            layout.addWidget(btn)
            self.botones_nav.append(btn)

        layout.addStretch()

        # Separador inferior
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #E5E7EB; margin: 0px 15px;")
        layout.addWidget(sep2)

        # Cerrar sesión
        btn_cerrar = QPushButton("🔄   Cerrar Sesión")
        btn_cerrar.setObjectName("btn_cerrar")
        btn_cerrar.setFixedHeight(42)
        btn_cerrar.clicked.connect(self._cerrar_sesion)
        layout.addWidget(btn_cerrar)

        # Salir
        btn_salir = QPushButton("🚪   Salir del Sistema")
        btn_salir.setObjectName("btn_salir")
        btn_salir.setFixedHeight(42)
        btn_salir.clicked.connect(self._salir)
        layout.addWidget(btn_salir)

        version = QLabel("v1.0.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setObjectName("version_label")
        version.setFixedHeight(28)
        layout.addWidget(version)

        return sidebar

    def _cargar_vistas(self):
        from ui.dashboard import DashboardView
        from ui.inventory_view import InventoryView
        from ui.alerts_view import AlertsView
        from ui.config_view import ConfigView

        self.dashboard_view = DashboardView(self.engine)
        self.inventory_view = InventoryView(self.engine)
        self.alerts_view    = AlertsView(self.engine)
        self.config_view    = ConfigView()

        self.contenido.addWidget(self.dashboard_view)
        self.contenido.addWidget(self.inventory_view)
        self.contenido.addWidget(self.alerts_view)
        self.contenido.addWidget(self.config_view)

        self._cambiar_vista(0)

    def _cambiar_vista(self, index: int):
        self.contenido.setCurrentIndex(index)
        for i, btn in enumerate(self.botones_nav):
            btn.setProperty("activo", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _escanear_automatico(self):
        resultados = self.engine.escanear_inventario()
        self.engine.aplicar_descuentos(resultados)
        if hasattr(self, "dashboard_view"):
            self.dashboard_view.actualizar(resultados)
        if hasattr(self, "alerts_view"):
            self.alerts_view.actualizar(resultados)

    def _cerrar_sesion(self):
        respuesta = QMessageBox.question(
            self, "Cerrar Sesión",
            "¿Deseas cerrar sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if respuesta == QMessageBox.StandardButton.Yes:
            self.close()
            from ui.login import LoginWindow
            self.login = LoginWindow()
            self.login.login_exitoso.connect(self._reabrir)
            self.login.show()

    def _reabrir(self, usuario):
        self.nueva_ventana = MainWindow(usuario)
        self.nueva_ventana.show()

    def _salir(self):
        respuesta = QMessageBox.question(
            self, "Salir",
            "¿Estás seguro de que deseas salir?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if respuesta == QMessageBox.StandardButton.Yes:
            import sys
            sys.exit(0)

    def _aplicar_estilos(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #F3F4F6; }
            QWidget     { background-color: #F3F4F6; color: #111827; font-family: Segoe UI; }

            #sidebar {
                background-color: #FFFFFF;
                border-right: 1px solid #E5E7EB;
            }
            #sidebar_header {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E5E7EB;
            }
            #sidebar_titulo {
                color: #1E40AF;
                font-size: 15px;
                font-weight: bold;
            }
            #usuario_lbl {
                color: #6B7280;
                font-size: 12px;
                background-color: #F9FAFB;
                padding: 5px;
                border-bottom: 1px solid #E5E7EB;
            }
            #nav_btn {
                background-color: transparent;
                color: #6B7280;
                font-size: 13px;
                font-weight: bold;
                text-align: left;
                padding-left: 20px;
                border: none;
                border-radius: 0px;
            }
            #nav_btn:hover {
                background-color: #F3F4F6;
                color: #1D4ED8;
            }
            #nav_btn[activo=true] {
                background-color: #EFF6FF;
                color: #1D4ED8;
                border-left: 3px solid #2563EB;
                font-weight: bold;
            }
            #btn_cerrar {
                background-color: #FFFFFF;
                color: #D97706;
                font-size: 12px;
                font-weight: bold;
                text-align: left;
                padding-left: 20px;
                border: none;
                border-top: 1px solid #F3F4F6;
            }
            #btn_cerrar:hover { background-color: #FFFBEB; }
            #btn_salir {
                background-color: #FFFFFF;
                color: #DC2626;
                font-size: 12px;
                font-weight: bold;
                text-align: left;
                padding-left: 20px;
                border: none;
            }
            #btn_salir:hover { background-color: #FEF2F2; }
            #version_label {
                color: #9CA3AF;
                font-size: 11px;
                background-color: #FFFFFF;
                border-top: 1px solid #F3F4F6;
            }
            QScrollArea { background-color: transparent; border: none; }
            QScrollBar:vertical {
                background-color: #F3F4F6;
                width: 5px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background-color: #D1D5DB;
                border-radius: 3px;
            }
        """)