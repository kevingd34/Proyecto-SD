from database import inicializar_bd
from models import Producto
from database import get_session
from risk_engine import RiskEngine
from datetime import datetime, timedelta

inicializar_bd()
session = get_session()

# Agregar productos de prueba con distintos riesgos
productos_prueba = [
    Producto(nombre="Leche Entera",    categoria="Lácteos",   precio_base=2500, stock=30, stock_maximo=50, fecha_vencimiento=datetime.now() + timedelta(days=2)),
    Producto(nombre="Pan Integral",    categoria="Panadería", precio_base=1800, stock=5,  stock_maximo=30, fecha_vencimiento=datetime.now() + timedelta(days=6)),
    Producto(nombre="Arroz 1kg",       categoria="Granos",    precio_base=3200, stock=95, stock_maximo=100),
    Producto(nombre="Jugo de Naranja", categoria="Bebidas",   precio_base=4000, stock=20, stock_maximo=40, fecha_vencimiento=datetime.now() + timedelta(days=15)),
]

session.add_all(productos_prueba)
session.commit()
session.close()

# Ejecutar el motor
engine = RiskEngine()
resultados = engine.escanear_inventario()
descuentos = engine.aplicar_descuentos(resultados)

# Mostrar resultados
print("\n" + "="*50)
print("       REPORTE DE RIESGO DE INVENTARIO")
print("="*50)

for nivel, items in resultados.items():
    if items:
        print(f"\n🔴 {nivel.upper()} ({len(items)} productos):")
        for item in items:
            print(f"  → {item['nombre']}")
            print(f"     Motivo   : {item['motivo']}")
            print(f"     Descuento: {item['descuento_sugerido']}%")
            print(f"     Precio   : ${item['precio_original']} → ${item['precio_sugerido']}")

print(f"\n✅ Descuentos aplicados en BD: {descuentos}")
engine.cerrar()