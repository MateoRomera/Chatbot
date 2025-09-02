from __future__ import annotations
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Carpeta con las fuentes de datos. Puedes usar DEFENSA_DATA_DIR o PERSONAL_DATA_DIR
DATA_DIR = Path(
    os.environ.get("DEFENSA_DATA_DIR")
    or os.environ.get("PERSONAL_DATA_DIR")
    or (ROOT / "data")
).resolve()

DEBUG = os.environ.get("DEFENSA_DEBUG", "0") == "1"
MAX_PREVIEW_ROWS = int(
    os.environ.get("DEFENSA_MAX_PREVIEW", "300")
)  # para tabla/light preview
CORS_ORIGINS = os.environ.get(
    "DEFENSA_CORS", "http://127.0.0.1:5173,http://localhost:5173"
).split(",")

# Columnas canónicas (orden recomendado en salidas)
CANON = [
    "ID",
    "Nombre completo",
    "DNI",
    "Fuerza",
    "Región",
    "Provincia",
    "Especialidad",
    "Formación universitaria",
    "Grado o Rango",
    "Destacamento",
    "Jefe inmediato",
    "Teléfono",
    "Correo electrónico",
]
