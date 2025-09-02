"""
data_loader.py
---------------
Loads personal datasets from multiple formats (CSV, JSON, XLSX, SQLite, PostgreSQL)
and prepares them for ingestion into RAGEngine.
"""

import os
import json
import sqlite3
import hashlib
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# 🔑 Base directory for datasets
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def verify_checksums(checksum_file: str = None) -> bool:
    if not checksum_file or not os.path.exists(checksum_file):
        return True
    with open(checksum_file, "r") as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 2:
            continue
        expected_hash, filename = parts
        filepath = os.path.join(DATA_DIR, os.path.basename(filename))
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            if file_hash != expected_hash:
                raise ValueError(f"Checksum mismatch for {filename}")
    return True

def load_csv(path: str) -> list[str]:
    df = pd.read_csv(path)
    return [row_to_text(r) for _, r in df.iterrows()]

def load_json(path: str) -> list[str]:
    with open(path, "r") as f:
        data = json.load(f)
    if isinstance(data, list):
        return [row_to_text(r) for r in data]
    elif isinstance(data, dict) and "records" in data:
        return [row_to_text(r) for r in data["records"]]
    elif isinstance(data, dict):  # diccionario anidado tipo {"1": {...}, "2": {...}}
        return [row_to_text(v) for v in data.values()]
    return []

def load_xlsx(path: str) -> list[str]:
    df = pd.read_excel(path)
    return [row_to_text(r) for _, r in df.iterrows()]

def load_sqlite(path: str, table: str = "personal") -> list[str]:
    conn = sqlite3.connect(path)
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return [row_to_text(r) for _, r in df.iterrows()]

def load_postgres(table: str = "personal", limit: int = 300) -> list[str]:
    """
    Load records from PostgreSQL table and convert to text.
    Uses credentials from environment variables (.env file).
    """
    try:
        user = os.getenv("PG_USER")
        password = os.getenv("PG_PASSWORD")
        host = os.getenv("PG_HOST", "localhost")
        port = os.getenv("PG_PORT", "5432")
        db = os.getenv("PG_DB")

        if not all([user, password, db]):
            print("⚠️ PostgreSQL credentials not set, skipping...")
            return []

        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
        engine = create_engine(url)

        query = f"SELECT * FROM {table} LIMIT {limit};"
        df = pd.read_sql(query, engine)

        return [row_to_text(r) for _, r in df.iterrows()]
    except Exception as e:
        print(f"❌ Could not load PostgreSQL table {table}: {e}")
        return []

def row_to_text(record) -> str:
    """
    Convert a record (Series or dict) into a human-readable string for embeddings.
    """
    try:
        if isinstance(record, dict):
            rec = {str(k).lower(): v for k, v in record.items()}
        else:  # pandas Series
            rec = {str(k).lower(): v for k, v in record.to_dict().items()}

        nombre = rec.get("nombre completo", "")
        dni = rec.get("dni", "")
        fuerza = rec.get("fuerza", "")
        provincia = rec.get("provincia", "")
        especialidad = rec.get("especialidad", "")
        formacion = rec.get("formación universitaria", "") or rec.get("formacion", "")

        return f"{nombre}, DNI {dni}, {especialidad} de la {fuerza} en {provincia}, con formación en {formacion}"
    except Exception as e:
        return f"[Unparsed record] {record} ({e})"

def load_all_data() -> list[str]:
    """
    Load all available data sources from /data folder and PostgreSQL (optional).
    """
    all_records = []
    checksum_file = os.path.join(DATA_DIR, "checksums.sha256")
    verify_checksums(checksum_file if os.path.exists(checksum_file) else None)

    for filename in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, filename)
        if filename.endswith(".csv"):
            all_records.extend(load_csv(path))
        elif filename.endswith(".json") and not filename.endswith(".tinydb.json"):
            all_records.extend(load_json(path))
        elif filename.endswith(".xlsx"):
            all_records.extend(load_xlsx(path))
        elif filename.endswith(".sqlite") or filename.endswith(".db"):
            all_records.extend(load_sqlite(path))

    # ✅ PostgreSQL (solo si está habilitado en .env)
    if os.getenv("PG_ENABLE", "0") == "1":
        all_records.extend(load_postgres(table="personal"))

    return all_records
