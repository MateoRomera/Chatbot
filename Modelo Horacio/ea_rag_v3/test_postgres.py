"""
test_postgres.py
----------------
Verify PostgreSQL connection and print first 5 rows from 'personal'.
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load env vars from .env
load_dotenv()

def test_postgres():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PG_DB", "ea_rag"),
            user=os.getenv("PG_USER", "horacio"),
            password=os.getenv("PG_PASSWORD", ""),
            host=os.getenv("PG_HOST", "localhost"),
            port=os.getenv("PG_PORT", "5432"),
        )
        cur = conn.cursor()
        print("✅ Connected to PostgreSQL")

        # Count rows
        cur.execute("SELECT COUNT(*) FROM personal;")
        total = cur.fetchone()[0]
        print(f"📊 Total records in table 'personal': {total}")

        # Show first 5 rows (now using snake_case column names)
        cur.execute("""
            SELECT nombre_completo, dni, fuerza, provincia, especialidad, formacion_universitaria
            FROM personal
            LIMIT 5;
        """)
        rows = cur.fetchall()
        print("\n--- Sample rows ---")
        for i, row in enumerate(rows, start=1):
            nombre, dni, fuerza, provincia, especialidad, formacion = row
            print(f"{i}. {nombre}, DNI {dni}, {especialidad} de la {fuerza} en {provincia}, con formación en {formacion}")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_postgres()
