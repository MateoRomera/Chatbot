# -*- coding: utf-8 -*-
"""
Backend v3 — fullstack_datalake_defensa_rag_v3

Endpoints:
  GET  /api/health
  GET  /api/meta/options
  POST /api/query/assisted
  POST /api/query/free
  POST /api/chat

Requisitos del entorno (requirements.txt recomendado):
  fastapi==0.115.0
  uvicorn[standard]==0.30.6
  pandas==2.3.1
  pyyaml==6.*
  duckdb==1.*
  xmltodict==0.13.*
  Unidecode==1.*  (si usás variantes; este archivo NO lo requiere)
"""

import os
import re
import json
import sqlite3
from pathlib import Path
from typing import Dict, List

import duckdb
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------------------------------
# Normalización y utilidades
# ---------------------------------------------------------------------


def _strip_accents(s: str) -> str:
    """Quita acentos y normaliza espacios/puntuación -> minúsculas."""
    import unicodedata

    if s is None:
        return ""
    s = str(s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# columnas que queremos conservar y en qué orden mostrarlas
KEEP_ORDER = [
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
    "Fecha de nacimiento",
]
# columnas a tirar si aparecen
DROP_COLS = {
    "__origen__",
    "_origen",
    "  origen  ",
    "__source__",
    "source",
    "__orig__",
    "__origin__",
}

# límite para responder resultados (rendimiento del browser)
RESULT_LIMIT = 200


# ---------------------------------------------------------------------
# Carga de datos multi‑fuente
# ---------------------------------------------------------------------


def _read_json_like(p: Path) -> pd.DataFrame:
    obj = json.loads(p.read_text(encoding="utf-8"))
    # TinyDB {"_default": {"1": {...}, "2": {...}}}
    if isinstance(obj, dict) and "_default" in obj:
        rows = [
            v for _, v in sorted(obj["_default"].items(), key=lambda kv: int(kv[0]))
        ]
        return pd.DataFrame(rows)
    # Lista de dicts
    if isinstance(obj, list):
        return pd.DataFrame(obj)
    # Dict arbitrario -> intento de lista
    return pd.DataFrame([obj])


def _read_excel(p: Path) -> pd.DataFrame:
    # dtype=str para que DNI no pierda ceros a izquierda si hubiera
    return pd.read_excel(p, dtype=str)


def _read_sqlite(p: Path) -> pd.DataFrame:
    con = sqlite3.connect(str(p))
    try:
        df = pd.read_sql("select * from personal", con)
    finally:
        con.close()
    return df


def _read_duckdb(p: Path) -> pd.DataFrame:
    con = duckdb.connect(str(p))
    try:
        tables = [t[0] for t in con.execute("SHOW TABLES").fetchall()]
        if "personal" not in tables:
            # si no existe la tabla personal, no rompemos
            return pd.DataFrame()
        df = con.execute('select * from "personal"').df()
    finally:
        con.close()
    return df


def _read_yaml(p: Path) -> pd.DataFrame:
    try:
        import yaml
    except Exception:
        return pd.DataFrame()
    obj = yaml.safe_load(p.read_text(encoding="utf-8"))
    if isinstance(obj, list):
        return pd.DataFrame(obj)
    if isinstance(obj, dict):
        return pd.DataFrame([obj])
    return pd.DataFrame()


def _read_xml(p: Path) -> pd.DataFrame:
    try:
        import xmltodict
    except Exception:
        return pd.DataFrame()
    obj = xmltodict.parse(p.read_text(encoding="utf-8"))

    def first_list(x):
        if isinstance(x, list):
            return x
        if isinstance(x, dict):
            for v in x.values():
                y = first_list(v)
                if y is not None:
                    return y
        return None

    lst = first_list(obj) or []
    return pd.DataFrame(lst)


def _read_parquet(p: Path) -> pd.DataFrame:
    # Carga condicional (pyarrow/fastparquet)
    try:
        return pd.read_parquet(p)
    except Exception:
        return pd.DataFrame()


def _rename_standard(df: pd.DataFrame) -> pd.DataFrame:
    """Unifica nombres de columnas a las que necesitamos."""
    rename_map = {
        "nombre": "Nombre completo",
        "nombre_completo": "Nombre completo",
        "dni": "DNI",
        "fuerza": "Fuerza",
        "region": "Región",
        "provincia": "Provincia",
        "especialidad": "Especialidad",
        "formacion universitaria": "Formación universitaria",
        "formación universitaria": "Formación universitaria",
        "grado": "Grado o Rango",
        "rango": "Grado o Rango",
        "grado o rango": "Grado o Rango",
        "destino": "Destacamento",
        "destacamento": "Destacamento",
        "jefe inmediato": "Jefe inmediato",
        "telefono": "Teléfono",
        "teléfono": "Teléfono",
        "correo": "Correo electrónico",
        "correo electronico": "Correo electrónico",
        "correo electrónico": "Correo electrónico",
        "fecha de nacimiento": "Fecha de nacimiento",
        "fecha_nacimiento": "Fecha de nacimiento",
    }
    m2 = {}
    for c in list(df.columns):
        key = _strip_accents(c)
        m2[c] = rename_map.get(key, c)
    df = df.rename(columns=m2)

    # Crear columnas faltantes vacías
    for k in KEEP_ORDER:
        if k not in df.columns:
            df[k] = ""
    return df


def _ensure_names(df: pd.DataFrame) -> pd.DataFrame:
    """Completa 'Nombre completo' si viniera vacío (p.ej. derivándolo del correo)."""
    if "Nombre completo" not in df.columns:
        df["Nombre completo"] = ""

    mask = df["Nombre completo"].astype(str).str.strip().eq("")
    if mask.any() and "Correo electrónico" in df.columns:
        tmp = (
            df.loc[mask, "Correo electrónico"]
            .fillna("")
            .astype(str)
            .str.extract(r"^([^@]+)@", expand=False)
            .fillna("")
            .str.replace(r"[\._\-]+", " ", regex=True)
            .str.title()
        )
        df.loc[mask, "Nombre completo"] = tmp
    return df


def _validate_and_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza DNI, elimina duplicados, quita columnas de origen."""
    if "DNI" in df.columns:
        df["DNI"] = (
            df["DNI"].astype(str).str.replace(r"\D", "", regex=True).str.slice(0, 9)
        )
    # quitar columnas de origen
    for c in list(df.columns):
        if c in DROP_COLS or (c.startswith("__") and c.endswith("__")):
            df = df.drop(columns=[c])
    # ID si falta
    if "ID" not in df.columns:
        df.insert(0, "ID", range(1, len(df) + 1))
    # dedup por DNI si está, si no por (Nombre + Fuerza + Provincia)
    if "DNI" in df.columns:
        df = df.drop_duplicates(subset=["DNI"], keep="first")
    else:
        df = df.drop_duplicates(
            subset=[
                c for c in ["Nombre completo", "Fuerza", "Provincia"] if c in df.columns
            ],
            keep="first",
        )
    return df.reset_index(drop=True)


def load_all_sources(data_dir: Path) -> pd.DataFrame:
    """Lee todas las fuentes soportadas dentro de data_dir/personal_* y unifica."""
    frames: List[pd.DataFrame] = []
    if not data_dir.exists():
        return pd.DataFrame()

    for p in sorted(data_dir.glob("personal_*")):
        try:
            sfx = p.suffix.lower()
            if sfx == ".csv":
                df = pd.read_csv(p, dtype=str)
            elif sfx == ".json":
                df = _read_json_like(p)
            elif sfx in (".xlsx", ".xls"):
                df = _read_excel(p)
            elif sfx in (".sqlite", ".db"):
                df = _read_sqlite(p)
            elif sfx == ".duckdb":
                df = _read_duckdb(p)
            elif sfx in (".yaml", ".yml"):
                df = _read_yaml(p)
            elif sfx == ".xml":
                df = _read_xml(p)
            elif sfx == ".parquet":
                df = _read_parquet(p)
            else:
                # otros (docx, etc.) ignorados
                df = pd.DataFrame()

            if not df.empty:
                df = _rename_standard(df)
                df = _ensure_names(df)
                df = _validate_and_clean(df)
                frames.append(df)
        except Exception as ex:
            # no frenamos todo por una fuente problemática
            print(f"[load] Ignorando {p.name}: {ex}")

    if not frames:
        return pd.DataFrame(columns=KEEP_ORDER)

    all_df = pd.concat(frames, ignore_index=True)
    # aplicar de nuevo por si quedaron duplicados inter-fuente
    all_df = _validate_and_clean(all_df)
    # dejar solo columnas de interés (si hay alguna más, no molesta)
    for c in list(all_df.columns):
        if c in DROP_COLS or (c.startswith("__") and c.endswith("__")):
            all_df = all_df.drop(columns=[c])
    return all_df


# ---------------------------------------------------------------------
# Catálogo y filtrado
# ---------------------------------------------------------------------


def build_catalog(df: pd.DataFrame) -> Dict[str, List[Dict[str, str]]]:
    """Arma contadores para selects."""

    def counts(col: str, label: str) -> List[Dict[str, str]]:
        if col not in df.columns:
            return []
        s = df[col].fillna("").astype(str)
        vc = s.value_counts().sort_index()
        return [
            {label: idx, "Filas": int(n)} for idx, n in vc.items() if str(idx).strip()
        ]

    return {
        "Región": counts("Región", "Región"),
        "Fuerza": counts("Fuerza", "Fuerza"),
        "Formación universitaria": counts(
            "Formación universitaria", "Formación universitaria"
        ),
        "Provincia": counts("Provincia", "Provincia"),
        "Especialidad": counts("Especialidad", "Especialidad"),
        "Jefe inmediato": counts("Jefe inmediato", "Jefe inmediato"),
        "Nombre completo": counts("Nombre completo", "Nombre completo"),
    }


def apply_filters(filters: Dict[str, str], base_df: pd.DataFrame) -> pd.DataFrame:
    """Aplica filtros exactos y 'contiene' sobre Nombre completo."""
    df = base_df

    # Igualdad directa en campos canónicos
    for key in [
        "Fuerza",
        "Región",
        "Provincia",
        "Especialidad",
        "Formación universitaria",
        "Jefe inmediato",
        "Grado o Rango",
    ]:
        val = filters.get(key)
        if val:
            df = df[df[key].astype(str) == str(val)]

    # DNI exacto si viene
    if filters.get("DNI"):
        v = str(filters["DNI"])
        df = df[df["DNI"].astype(str) == v]

    # Nombre contiene (case/acentos insensitive)
    if filters.get("Nombre completo__contains"):
        needle = _strip_accents(filters["Nombre completo__contains"])
        if needle:
            sr = df["Nombre completo"].fillna("").astype(str).map(_strip_accents)
            df = df[sr.str.contains(re.escape(needle))]

    return df


def format_output(df: pd.DataFrame) -> List[Dict[str, str]]:
    """Ordena columnas y limita a RESULT_LIMIT; quita 'origen' y similares."""
    out = df.copy()
    for c in list(out.columns):
        if c in DROP_COLS or (c.startswith("__") and c.endswith("__")):
            out = out.drop(columns=[c])
    keep = [c for c in KEEP_ORDER if c in out.columns]
    out = out[keep]
    return out.head(RESULT_LIMIT).to_dict(orient="records")


# ---------------------------------------------------------------------
# App & endpoints
# ---------------------------------------------------------------------

app = FastAPI(title="Defensa v3")

# CORS para el front en 5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # si querés más estricto: ["http://127.0.0.1:5173","http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data global
DATA_DIR = Path(
    os.environ.get("DEFENSA_DATA_DIR", Path(__file__).resolve().parent / "data")
)
DATA = load_all_sources(DATA_DIR)
CATALOG = build_catalog(DATA)


@app.get("/api/health")
def health():
    return {"status": "ok", "rows": int(len(DATA))}


@app.get("/api/meta/options")
def meta_options():
    return {"options": CATALOG}


@app.post("/api/query/assisted")
def q_assisted(payload: Dict):
    filters = payload or {}
    df = apply_filters(filters, DATA)
    return {"count": int(len(df)), "results": format_output(df)}


# --- Parser SLM de lenguaje natural ---
try:
    # Debe existir en backend/src/slm_parser.py
    from src.slm_parser import parse_free
except Exception as ex:  # fallback mínimo si faltara el archivo
    print("[warn] No se pudo importar src.slm_parser.parse_free:", ex)

    def parse_free(text: str, catalog: Dict) -> Dict[str, str]:
        """Fallback muy básico (solo ejemplo). Reemplazar por el real si falta el archivo."""
        t = _strip_accents(text)
        f = {}
        if m := re.search(r"\b(\d{7,9})\b", t):
            f["DNI"] = m.group(1)
            return f
        if "ejercito" in t:
            f["Fuerza"] = "Ejército"
        if "armada" in t:
            f["Fuerza"] = "Armada"
        if "aerea" in t or "fuerza aerea" in t:
            f["Fuerza"] = "Fuerza Aérea"
        for it in catalog.get("Provincia", []):
            p = it.get("Provincia", "")
            if f" { _strip_accents(p) } " in f" {t} ":
                f["Provincia"] = p
                break
        # token como nombre contiene
        toks = [w for w in t.split() if len(w) >= 4]
        if toks:
            f["Nombre completo__contains"] = toks[0]
        return f


@app.post("/api/query/free")
def q_free(payload: Dict):
    text = (payload or {}).get("text", "")
    filters = parse_free(text, CATALOG)
    df = apply_filters(filters, DATA)
    return {"filters": filters, "count": int(len(df)), "results": format_output(df)}


@app.post("/api/chat")
def chat(payload: Dict):
    """Pequeño 'chat' local basado en filtros + estadísticas (RAG/SLM liviano)."""
    from collections import Counter

    msg = (payload or {}).get("message", "")
    filters = parse_free(msg, CATALOG)
    df = apply_filters(filters, DATA)
    n = len(df)

    by_force = Counter(df["Fuerza"]) if "Fuerza" in df.columns else Counter()
    by_spec = Counter(df["Especialidad"]) if "Especialidad" in df.columns else Counter()
    samples = list(df["Nombre completo"][:5]) if "Nombre completo" in df.columns else []

    parts = [f"Encontré {n} persona(s) con esos criterios."]
    if by_force:
        topf = ", ".join(f"{k}: {v}" for k, v in by_force.most_common(3))
        parts.append(f"Distribución por fuerza: {topf}.")
    if by_spec:
        tops = ", ".join(f"{k}: {v}" for k, v in by_spec.most_common(3))
        parts.append(f"Especialidades destacadas: {tops}.")
    if samples:
        parts.append(f"Ejemplos: {', '.join(samples)}.")
    return {
        "answer": " ".join(parts),
        "filters": filters,
        "count": n,
        "examples": samples,
    }


# ---------------------------------------------------------------------
# Arranque directo (opcional)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
