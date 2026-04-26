from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QScrollArea, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt

class AlertsView(QWidget):

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self._construir_ui()

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titulo = QLabel("🚨  Alertas de Inventario")
        titulo.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #DC2626;
        """)
        layout.addWidget(titulo)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")
        self.contenedor = QWidget()
        self.contenedor.setStyleSheet("background-color: transparent;")
        self.contenedor_layout = QVBoxLayout(self.contenedor)
        self.contenedor_layout.setSpacing(10)
        scroll.setWidget(self.contenedor)
        layout.addWidget(scroll)

    def actualizar(self, resultados: dict):
        while self.contenedor_layout.count():
            item = self.contenedor_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        niveles = {
            "critico": ("🔴  CRÍTICO",  "#DC2626", "#FEF2F2"),
            "alto":    ("🟠  ALTO",     "#D97706", "#FFFBEB"),
            "medio":   ("🟡  MEDIO",    "#CA8A04", "#FEFCE8"),
        }

        hay_alertas = False
        for nivel, (etiqueta, color, fondo) in niveles.items():
            items = resultados.get(nivel, [])
            if not items:
                continue

            hay_alertas = True

            encabezado = QLabel(f"{etiqueta}  —  {len(items)} producto(s)")
            encabezado.setStyleSheet(f"""
                color: {color};
                font-size: 13px;
                font-weight: bold;
                padding: 6px 0px;
            """)
            self.contenedor_layout.addWidget(encabezado)

            for item in items:
                self.contenedor_layout.addWidget(
                    self._crear_tarjeta(item, color, fondo)
                )

        if not hay_alertas:
            lbl = QLabel("✅  No hay alertas activas. ¡Todo el inventario está en orden!")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("""
                color: #16A34A;
                font-size: 14px;
                padding: 40px;
                background-color: #F0FDF4;
                border-radius: 8px;
            """)
            self.contenedor_layout.addWidget(lbl)

        self.contenedor_layout.addStretch()

    def _crear_tarjeta(self, item: dict, color: str, fondo: str) -> QFrame:
        tarjeta = QFrame()
        tarjeta.setStyleSheet(f"""
            QFrame {{
                background-color: {fondo};
                border-radius: 8px;
                border-left: 4px solid {color};
                border: 1px solid #E5E7EB;
                border-left: 4px solid {color};
            }}
        """)
        layout = QHBoxLayout(tarjeta)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(15)

        # Izquierda
        info = QVBoxLayout()
        nombre = QLabel(f"<b style='font-size:14px; color:#111827;'>{item['nombre']}</b>")
        motivo = QLabel(f"📋  {item['motivo']}")
        motivo.setStyleSheet("color: #6B7280; font-size: 12px;")
        stock  = QLabel(f"📦  Stock: {item['stock']} unidades")
        stock.setStyleSheet("color: #6B7280; font-size: 12px;")

        info.addWidget(nombre)
        info.addWidget(motivo)
        info.addWidget(stock)

        # Derecha
        precios = QVBoxLayout()
        precios.setAlignment(Qt.AlignmentFlag.AlignRight)

        badge = QLabel(f"-{item['descuento_sugerido']}% OFF")
        badge.setStyleSheet(f"""
            color: white;
            background-color: {color};
            font-weight: bold;
            font-size: 13px;
            padding: 4px 12px;
            border-radius: 12px;
        """)
        badge.setAlignment(Qt.AlignmentFlag.AlignRight)

        precio_orig = QLabel(f"Antes: ${item['precio_original']:,.0f}")
        precio_orig.setStyleSheet("color: #9CA3AF; text-decoration: line-through; font-size: 12px;")
        precio_orig.setAlignment(Qt.AlignmentFlag.AlignRight)

        precio_nuevo = QLabel(f"Ahora: ${item['precio_sugerido']:,.0f}")
        precio_nuevo.setStyleSheet("color: #16A34A; font-weight: bold; font-size: 13px;")
        precio_nuevo.setAlignment(Qt.AlignmentFlag.AlignRight)

        precios.addWidget(badge)
        precios.addWidget(precio_orig)
        precios.addWidget(precio_nuevo)

        layout.addLayout(info)
        layout.addStretch()
        layout.addLayout(precios)
        return tarjeta