import sys
import platform
from pathlib import Path
from platformdirs import user_data_dir, user_log_dir

# ── Información general de la app ──────────────────────────────────────────
APP_NAME        = "InventarioApp"
APP_AUTHOR      = "Johan"
APP_VERSION     = "1.0.0"

# ── Detectar sistema operativo ─────────────────────────────────────────────
SISTEMA = platform.system()   # 'Windows', 'Darwin' (macOS), 'Linux'

def es_windows() -> bool:
    return SISTEMA == "Windows"

def es_mac() -> bool:
    return SISTEMA == "Darwin"

def es_linux() -> bool:
    return SISTEMA == "Linux"

# ── Rutas dinámicas según el OS ────────────────────────────────────────────
# Carpeta principal donde se guardan los datos de la app
DATA_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))

# Carpeta de logs
LOG_DIR  = Path(user_log_dir(APP_NAME, APP_AUTHOR))

# Ruta de la base de datos
DB_PATH  = DATA_DIR / "inventario.db"

# Carpeta de reportes exportados
REPORTS_DIR = DATA_DIR / "reportes"

def crear_directorios():
    """Crea las carpetas necesarias si no existen."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Configuración general de la app ───────────────────────────────────────
CONFIG = {
    "moneda": "$",
    "dias_alerta_vencimiento": 7,      # Alertar si vence en menos de 7 días
    "dias_critico_vencimiento": 3,     # Crítico si vence en menos de 3 días
    "umbral_stock_bajo": 10,           # Alerta si stock menor a 10 unidades
    "descuento_critico": 50,           # 50% descuento en productos críticos
    "descuento_alto": 30,              # 30% descuento en riesgo alto
    "descuento_medio": 15,             # 15% descuento en riesgo medio
    "descuento_sobrestock": 10,        # 10% descuento por sobrestock
}

# ── Imprimir info al iniciar (útil para debug) ─────────────────────────────
if __name__ == "__main__":
    crear_directorios()
    print(f"Sistema operativo : {SISTEMA}")
    print(f"Versión Python    : {sys.version}")
    print(f"Carpeta de datos  : {DATA_DIR}")
    print(f"Base de datos     : {DB_PATH}")
    print(f"Reportes          : {REPORTS_DIR}")
    print(f"Logs              : {LOG_DIR}")