from __future__ import annotations
import json, sqlite3, xmltodict, yaml, duckdb, re
from pathlib import Path
import pandas as pd
from tinydb import TinyDB
from .config import DATA_DIR, DEBUG, CANON

# Provincias → Región
PROV_2_REGION = {
    # NOA
    "Jujuy": "NOA",
    "Salta": "NOA",
    "Tucumán": "NOA",
    "Catamarca": "NOA",
    "La Rioja": "NOA",
    "Santiago del Estero": "NOA",
    # NEA
    "Chaco": "NEA",
    "Formosa": "NEA",
    "Corrientes": "NEA",
    "Misiones": "NEA",
    # Centro
    "Buenos Aires": "Centro",
    "Ciudad Autónoma de Buenos Aires": "Centro",
    "Córdoba": "Centro",
    "Santa Fe": "Centro",
    "Entre Ríos": "Centro",
    "La Pampa": "Centro",
    # Cuyo
    "Mendoza": "Cuyo",
    "San Juan": "Cuyo",
    "San Luis": "Cuyo",
    # Patagonia
    "Neuquén": "Patagonia",
    "Río Negro": "Patagonia",
    "Chubut": "Patagonia",
    "Santa Cruz": "Patagonia",
    "Tierra del Fuego": "Patagonia",
    # Opcionales
    "Provincia de Buenos Aires": "Centro",
}

RENAMES = {
    "nombre": "Nombre completo",
    "nombre completo": "Nombre completo",
    "dni": "DNI",
    "correo": "Correo electrónico",
    "email": "Correo electrónico",
    "tel": "Teléfono",
    "telefono": "Teléfono",
    "teléfono": "Teléfono",
    "grado": "Grado o Rango",
    "rango": "Grado o Rango",
    "region": "Región",
    "provincia": "Provincia",
    "destacamento": "Destacamento",
    "fuerza": "Fuerza",
    "especialidad": "Especialidad",
    "formación universitaria": "Formación universitaria",
    "formacion universitaria": "Formación universitaria",
    "jefe inmediato": "Jefe inmediato",
}


def _canon_cols(df: pd.DataFrame) -> pd.DataFrame:
    # normaliza nombres de columnas (case-insensitive, acentos fuera)
    def norm(s: str) -> str:
        import unicodedata

        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
        return s.strip().lower()

    mapping = {}
    for c in df.columns:
        k = norm(str(c))
        mapping[c] = RENAMES.get(k, c)
    df = df.rename(columns=mapping)

    # Si falta Región, la inferimos por Provincia
    if "Región" not in df.columns and "Provincia" in df.columns:
        df["Región"] = df["Provincia"].map(PROV_2_REGION)

    # Aseguramos columnas canónicas
    for c in CANON:
        if c not in df.columns:
            df[c] = pd.NA

    # DNI a texto, limpio
    if "DNI" in df.columns:
        df["DNI"] = df["DNI"].astype(str).str.replace(r"\D", "", regex=True).str[:8]

    # Relleno de "Nombre completo" desde email si viene vacío
    if "Nombre completo" in df.columns and "Correo electrónico" in df.columns:
        mask = df["Nombre completo"].isna() | (
            df["Nombre completo"].astype(str).str.strip() == ""
        )
        if mask.any():
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

    # Limpieza general
    for c in df.columns:
        df[c] = df[c].astype(str).str.strip()

    return df


def _read_csv(p: Path) -> pd.DataFrame:
    return pd.read_csv(p, dtype=str, keep_default_na=False)


def _read_json(p: Path) -> pd.DataFrame:
    obj = json.loads(Path(p).read_text(encoding="utf-8"))
    # TinyDB-like: {"_default": {"1":{...}, ...}}
    if isinstance(obj, dict) and "_default" in obj:
        rows = [
            v for _, v in sorted(obj["_default"].items(), key=lambda kv: int(kv[0]))
        ]
        return pd.DataFrame(rows)
    # Lista de dicts
    if isinstance(obj, list):
        return pd.DataFrame(obj)
    # Dict plano
    return pd.DataFrame([obj])


def _read_xlsx(p: Path) -> pd.DataFrame:
    return pd.read_excel(p, dtype=str)


def _read_parquet(p: Path) -> pd.DataFrame:
    # requiere pyarrow instalado
    return pd.read_parquet(p)


def _read_sqlite(p: Path) -> pd.DataFrame:
    con = sqlite3.connect(str(p))
    try:
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", con)[
            "name"
        ].tolist()
        table = "personal" if "personal" in tables else (tables[0] if tables else None)
        if not table:
            return pd.DataFrame()
        return pd.read_sql(f'SELECT * FROM "{table}"', con)
    finally:
        con.close()


def _read_duckdb(p: Path) -> pd.DataFrame:
    con = duckdb.connect(str(p))
    try:
        tables = [r[0] for r in con.execute("SHOW TABLES").fetchall()]
        table = "personal" if "personal" in tables else (tables[0] if tables else None)
        if not table:
            return pd.DataFrame()
        return con.execute(f'SELECT * FROM "{table}"').df()
    finally:
        con.close()


def _read_yaml(p: Path) -> pd.DataFrame:
    obj = yaml.safe_load(Path(p).read_text(encoding="utf-8"))
    if isinstance(obj, list):
        return pd.DataFrame(obj)
    if isinstance(obj, dict) and "_default" in obj:
        rows = [
            v for _, v in sorted(obj["_default"].items(), key=lambda kv: int(kv[0]))
        ]
        return pd.DataFrame(rows)
    return pd.DataFrame([obj])


def _read_xml(p: Path) -> pd.DataFrame:
    obj = xmltodict.parse(Path(p).read_text(encoding="utf-8"))

    # intentamos encontrar una lista de elementos
    def flatten(x):
        if isinstance(x, list):
            return x
        if isinstance(x, dict):
            for v in x.values():
                y = flatten(v)
                if y is not None:
                    return y
        return None

    rows = flatten(obj) or []
    return pd.DataFrame(rows)


READERS = {
    ".csv": _read_csv,
    ".json": _read_json,
    ".xlsx": _read_xlsx,
    ".xls": _read_xlsx,
    ".sqlite": _read_sqlite,
    ".db": _read_sqlite,
    ".duckdb": _read_duckdb,
    ".yaml": _read_yaml,
    ".yml": _read_yaml,
    ".xml": _read_xml,
    ".parquet": _read_parquet,
}


def discover_sources(folder: Path) -> list[Path]:
    exts = set(READERS.keys())
    return [p for p in folder.glob("*") if p.suffix.lower() in exts and p.is_file()]


def load_all() -> pd.DataFrame:
    folder = DATA_DIR
    folder.mkdir(parents=True, exist_ok=True)
    dfs = []
    for p in discover_sources(folder):
        try:
            df = READERS[p.suffix.lower()](p)
            if df.empty:
                continue
            df = _canon_cols(df)
            df["__origen__"] = str(p)  # interno; no se expone al front
            dfs.append(df)
        except Exception as e:
            if DEBUG:
                print(f"[warn] no pude leer {p}: {e}")

    if not dfs:
        return pd.DataFrame(columns=CANON)

    all_df = pd.concat(dfs, ignore_index=True)

    # deduplicado por DNI si está válido (7-8 dígitos)
    if "DNI" in all_df.columns:
        mask = all_df["DNI"].str.fullmatch(r"\d{7,8}", na=False)
        all_df = pd.concat(
            [all_df[mask].drop_duplicates(subset=["DNI"]), all_df[~mask]],
            ignore_index=True,
        )

    # orden de columnas
    left = [c for c in CANON if c in all_df.columns]
    rest = [c for c in all_df.columns if c not in left and c != "__origen__"]
    return all_df[left + rest + ["__origen__"]]


def catalogs(df: pd.DataFrame) -> dict[str, list[str]]:
    cats = {}
    for col in [
        "Región",
        "Fuerza",
        "Provincia",
        "Especialidad",
        "Formación universitaria",
        "Jefe inmediato",
        "Nombre completo",
    ]:
        if col in df.columns:
            vals = (
                df[col]
                .dropna()
                .astype(str)
                .str.strip()
                .replace("", pd.NA)
                .dropna()
                .unique()
                .tolist()
            )
            vals.sort()
            cats[col] = vals
    return cats
