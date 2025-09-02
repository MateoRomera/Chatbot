import sqlite3
import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
db_path = os.path.join(DATA_DIR, "personal_f.sqlite")

# Crear DataFrame de ejemplo
records = []
for i in range(300):
    records.append({
        "ID": 2000 + i,
        "Nombre completo": f"Test User {i+1}",
        "DNI": f"{30000000+i}",
        "Fuerza": "Ejército" if i % 2 == 0 else "Armada",
        "Provincia": "Buenos Aires" if i % 3 == 0 else "Mendoza",
        "Especialidad": "Ingeniero" if i % 5 == 0 else "Médico",
        "Formación universitaria": "Historia" if i % 7 == 0 else "Geografía"
    })

df = pd.DataFrame(records)

# Guardar en SQLite
conn = sqlite3.connect(db_path)
df.to_sql("personal", conn, if_exists="replace", index=False)
conn.close()

print(f"✅ Base creada en {db_path} con {len(records)} registros")
