from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt

class DashboardView(QWidget):

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self._construir_ui()

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Título
        titulo = QLabel("📊  Dashboard")
        titulo.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #1E40AF;
        """)
        layout.addWidget(titulo)

        # Tarjetas
        self.tarjetas_layout = QHBoxLayout()
        self.tarjetas_layout.setSpacing(12)
        layout.addLayout(self.tarjetas_layout)

        # Subtítulo
        subtitulo = QLabel("Productos que requieren atención")
        subtitulo.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #6B7280;
            padding-top: 5px;
        """)
        layout.addWidget(subtitulo)

        # Lista con scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")
        self.lista_widget = QWidget()
        self.lista_widget.setStyleSheet("background-color: transparent;")
        self.lista_layout = QVBoxLayout(self.lista_widget)
        self.lista_layout.setSpacing(8)
        scroll.setWidget(self.lista_widget)
        layout.addWidget(scroll)

    def actualizar(self, resultados: dict):
        # Limpiar tarjetas
        while self.tarjetas_layout.count():
            item = self.tarjetas_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        criticos = len(resultados.get("critico", []))
        altos    = len(resultados.get("alto", []))
        medios   = len(resultados.get("medio", []))
        normales = len(resultados.get("normal", []))
        total    = criticos + altos + medios + normales

        # Todas las tarjetas en gris neutro, solo cambia el ícono
        tarjetas = [
            ("Total Productos", str(total),    "📦"),
            ("Críticos",        str(criticos), "🔴"),
            ("Riesgo Alto",     str(altos),    "🟠"),
            ("Riesgo Medio",    str(medios),   "🟡"),
        ]

        for titulo, valor, icono in tarjetas:
            self.tarjetas_layout.addWidget(
                self._crear_tarjeta(titulo, valor, icono)
            )

        # Limpiar lista
        while self.lista_layout.count():
            item = self.lista_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Pastel suave por nivel
        niveles = {
            "critico": ("#FECACA", "#991B1B", "Crítico"),
            "alto":    ("#FED7AA", "#9A3412", "Alto"),
            "medio":   ("#FEF08A", "#854D0E", "Medio"),
        }

        hay_riesgo = False
        for nivel, (pastel, texto, etiqueta) in niveles.items():
            for item in resultados.get(nivel, []):
                self.lista_layout.addWidget(
                    self._crear_fila(item, pastel, texto, etiqueta)
                )
                hay_riesgo = True

        if not hay_riesgo:
            lbl = QLabel("✅  Todo el inventario está en estado normal")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("""
                color: #166534;
                font-size: 14px;
                padding: 30px;
                background-color: #DCFCE7;
                border-radius: 8px;
                border: 1px solid #BBF7D0;
            """)
            self.lista_layout.addWidget(lbl)

        self.lista_layout.addStretch()

    def _crear_tarjeta(self, titulo, valor, icono) -> QFrame:
        tarjeta = QFrame()
        tarjeta.setFixedHeight(95)
        tarjeta.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 10px;
                border: 1px solid #E5E7EB;
            }
            QFrame:hover {
                border: 1px solid #D1D5DB;
                background-color: #F9FAFB;
            }
        """)
        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(4)

        lbl_titulo = QLabel(f"{icono}  {titulo}")
        lbl_titulo.setStyleSheet("""
            color: #6B7280;
            font-size: 12px;
            font-weight: bold;
        """)

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet("""
            color: #111827;
            font-size: 32px;
            font-weight: bold;
        """)

        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_valor)
        return tarjeta

    def _crear_fila(self, item: dict, pastel: str, texto: str, etiqueta: str) -> QFrame:
        fila = QFrame()
        fila.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 8px;
                border: 1px solid #E5E7EB;
            }
        """)
        layout = QHBoxLayout(fila)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(12)

        # Badge nivel en pastel
        badge_nivel = QLabel(etiqueta)
        badge_nivel.setFixedWidth(55)
        badge_nivel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge_nivel.setStyleSheet(f"""
            color: {texto};
            background-color: {pastel};
            font-size: 11px;
            font-weight: bold;
            padding: 3px 6px;
            border-radius: 6px;
        """)

        # Nombre y motivo
        info = QVBoxLayout()
        info.setSpacing(2)
        nombre = QLabel(f"<b style='color:#111827; font-size:13px;'>{item['nombre']}</b>")
        motivo = QLabel(f"<span style='color:#9CA3AF; font-size:11px;'>{item['motivo']}</span>")
        info.addWidget(nombre)
        info.addWidget(motivo)

        # Descuento badge pastel
        badge_desc = QLabel(f"-{item['descuento_sugerido']}%")
        badge_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge_desc.setStyleSheet("""
            color: #1D4ED8;
            background-color: #DBEAFE;
            font-size: 12px;
            font-weight: bold;
            padding: 4px 10px;
            border-radius: 6px;
        """)

        # Precios
        precio = QLabel(
            f"<span style='color:#9CA3AF; font-size:11px; "
            f"text-decoration:line-through;'>${item['precio_original']:,.0f}</span>"
            f"  <b style='color:#15803D; font-size:13px;'>${item['precio_sugerido']:,.0f}</b>"
        )
        precio.setTextFormat(Qt.TextFormat.RichText)
        precio.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(badge_nivel)
        layout.addLayout(info)
        layout.addStretch()
        layout.addWidget(badge_desc)
        layout.addWidget(precio)
        return fila