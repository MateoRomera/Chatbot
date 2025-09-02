"""
populate_postgres.py
---------------------
Populate PostgreSQL 'personal' table from CSV/JSON/SQLite datasets with normalized snake_case columns.
"""

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

PG_CONN = dict(
    dbname=os.getenv("PG_DB", "ea_rag"),
    user=os.getenv("PG_USER", "horacio"),
    password=os.getenv("PG_PASSWORD", ""),
    host=os.getenv("PG_HOST", "localhost"),
    port=os.getenv("PG_PORT", "5432"),
)

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "personal_a.csv")

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("ó", "o")
        .str.replace("í", "i")
        .str.replace("á", "a")
        .str.replace("é", "e")
        .str.replace("ú", "u")
    )
    return df

def main():
    try:
        # Load sample CSV
        df = pd.read_csv(DATA_FILE)
        df = normalize_columns(df)

        conn = psycopg2.connect(**PG_CONN)
        cur = conn.cursor()

        # Drop and recreate table
        cur.execute("DROP TABLE IF EXISTS personal;")
        cur.execute("""
            CREATE TABLE personal (
                id SERIAL PRIMARY KEY,
                nombre_completo TEXT,
                dni TEXT,
                fecha_nacimiento TEXT,
                fuerza TEXT,
                grado_o_rango TEXT,
                region TEXT,
                provincia TEXT,
                destacamento TEXT,
                formacion_universitaria TEXT,
                capacitacion TEXT,
                especialidad TEXT,
                jefe_inmediato TEXT,
                telefono TEXT,
                correo_electronico TEXT
            );
        """)

        # Insert rows
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO personal (
                    nombre_completo, dni, fecha_nacimiento, fuerza, grado_o_rango,
                    region, provincia, destacamento, formacion_universitaria,
                    capacitacion, especialidad, jefe_inmediato, telefono, correo_electronico
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                row.get("nombre_completo"), row.get("dni"), row.get("fecha_de_nacimiento"),
                row.get("fuerza"), row.get("grado_o_rango"), row.get("region"), row.get("provincia"),
                row.get("destacamento"), row.get("formacion_universitaria"),
                row.get("capacitacion"), row.get("especialidad"), row.get("jefe_inmediato"),
                row.get("telefono"), row.get("correo_electronico"),
            ))

        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ PostgreSQL table 'personal' repoblada con {len(df)} registros normalizados.")

    except Exception as e:
        print(f"❌ Error populating PostgreSQL: {e}")

if __name__ == "__main__":
    main()
