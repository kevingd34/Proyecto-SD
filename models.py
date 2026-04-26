from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import hashlib
from database import Base

class NivelRiesgo(enum.Enum):
    NORMAL   = "normal"
    MEDIO    = "medio"
    ALTO     = "alto"
    CRITICO  = "critico"

# ── Tabla de Usuarios ──────────────────────────────────────────────────────
class Usuario(Base):
    __tablename__ = "usuarios"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    nombre   = Column(String(100), nullable=False)
    usuario  = Column(String(50),  nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    rol      = Column(String(20),  default="usuario")  # admin / usuario
    activo   = Column(Integer,     default=1)

    @staticmethod
    def hashear_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verificar_password(self, password: str) -> bool:
        return self.password == hashlib.sha256(password.encode()).hexdigest()

    def __repr__(self):
        return f"<Usuario {self.usuario} | Rol: {self.rol}>"

# ── Tabla de Productos ─────────────────────────────────────────────────────
class Producto(Base):
    __tablename__ = "productos"

    id                = Column(Integer, primary_key=True, autoincrement=True)
    nombre            = Column(String(100), nullable=False)
    categoria         = Column(String(50),  nullable=False)
    precio_base       = Column(Float,       nullable=False)
    stock             = Column(Integer,     nullable=False, default=0)
    stock_maximo      = Column(Integer,     nullable=False, default=100)
    fecha_vencimiento = Column(DateTime,    nullable=True)
    fecha_ingreso     = Column(DateTime,    default=datetime.now)
    nivel_riesgo      = Column(String(20),  default=NivelRiesgo.NORMAL.value)
    activo            = Column(Integer,     default=1)

    ventas     = relationship("Venta",     back_populates="producto")
    descuentos = relationship("Descuento", back_populates="producto")

    def __repr__(self):
        return f"<Producto {self.nombre} | Stock: {self.stock} | Riesgo: {self.nivel_riesgo}>"

# ── Tabla de Ventas ────────────────────────────────────────────────────────
class Venta(Base):
    __tablename__ = "ventas"

    id                 = Column(Integer, primary_key=True, autoincrement=True)
    producto_id        = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad           = Column(Integer, nullable=False)
    precio_unitario    = Column(Float,   nullable=False)
    precio_final       = Column(Float,   nullable=False)
    descuento_aplicado = Column(Float,   default=0.0)
    fecha              = Column(DateTime, default=datetime.now)

    producto = relationship("Producto", back_populates="ventas")

# ── Tabla de Descuentos ────────────────────────────────────────────────────
class Descuento(Base):
    __tablename__ = "descuentos"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    porcentaje  = Column(Float,   nullable=False)
    motivo      = Column(String(200), nullable=False)
    activo      = Column(Integer, default=1)
    fecha_inicio= Column(DateTime, default=datetime.now)
    fecha_fin   = Column(DateTime, nullable=True)

    producto = relationship("Producto", back_populates="descuentos")