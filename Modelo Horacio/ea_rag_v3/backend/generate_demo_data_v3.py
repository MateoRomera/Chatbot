import os
import pandas as pd
import sqlite3
import json
import hashlib

DATA_DIR = os.path.join("backend", "data")
os.makedirs(DATA_DIR, exist_ok=True)
N = 650  # filas por dataset

def generar_datos(base_name: str, n: int, offset: int):
    return pd.DataFrame({
        "dni": range(offset, offset + n),
        "nombre": [f"{base_name}_Nombre_{i}" for i in range(n)],
        "apellido": [f"{base_name}_Apellido_{i}" for i in range(n)],
        "fuerza": [base_name for _ in range(n)],
        "provincia": ["Córdoba" if i % 2 == 0 else "Buenos Aires" for i in range(n)]
    })

def sha256sum(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

datasets = {
    "personal_a": generar_datos("Ejercito", N, 100000),
    "personal_b": generar_datos("Armada", N, 200000),
    "personal_c": generar_datos("FuerzaAerea", N, 300000),
    "personal_e": generar_datos("Gendarmeria", N, 400000),
    "personal_f": generar_datos("Prefectura", N, 500000),
    "personal_g": generar_datos("PoliciaFederal", N, 600000),
}

checksums = {}

for name, df in datasets.items():
    csv_path = os.path.join(DATA_DIR, f"{name}.csv")
    json_path = os.path.join(DATA_DIR, f"{name}.json")

    print(f"Generando {csv_path}...", end=" ", flush=True)
    df.to_csv(csv_path, index=False)
    print("OK")
    checksums[csv_path] = sha256sum(csv_path)

    print(f"Generando {json_path}...", end=" ", flush=True)
    df.to_json(json_path, orient="records", indent=2, force_ascii=False)
    print("OK")
    checksums[json_path] = sha256sum(json_path)

    if name == "personal_c":
        xlsx_path = os.path.join(DATA_DIR, f"{name}.xlsx")
        print(f"Generando {xlsx_path}...", end=" ", flush=True)
        df.to_excel(xlsx_path, index=False)
        print("OK")
        checksums[xlsx_path] = sha256sum(xlsx_path)

    if name == "personal_e":
        sqlite_path = os.path.join(DATA_DIR, f"{name}.sqlite")
        print(f"Generando {sqlite_path}...", end=" ", flush=True)
        conn = sqlite3.connect(sqlite_path)
        # 🔹 Guardamos la tabla con nombre fijo "personal"
        df.to_sql("personal", conn, if_exists="replace", index=False)
        conn.close()
        print("OK")
        checksums[sqlite_path] = sha256sum(sqlite_path)

    if name == "personal_f":
        tinydb_path = os.path.join(DATA_DIR, f"{name}_tinydb.json")
        print(f"Generando {tinydb_path}...", end=" ", flush=True)
        with open(tinydb_path, "w", encoding="utf-8") as f:
            json.dump(df.to_dict(orient="records"), f, indent=2, ensure_ascii=False)
        print("OK")
        checksums[tinydb_path] = sha256sum(tinydb_path)

# Resumen de filas y verificación
all_dnis = pd.concat([df["dni"] for df in datasets.values()])
total = len(all_dnis)
unique = all_dnis.nunique()
print("--------------------------------------------------")
print(f"Total de registros generados: {total}")
print(f"DNIs únicos: {unique}")
if total == unique:
    print("✅ Verificación OK: no hay duplicados en ningún dataset.")
else:
    print("❌ Atención: se encontraron duplicados en los DNIs.")
print("--------------------------------------------------")

# Guardar checksums
checksums_file = os.path.join(DATA_DIR, "checksums.sha256")
with open(checksums_file, "w", encoding="utf-8") as f:
    for file, h in checksums.items():
        line = f"{h}  {os.path.basename(file)}"
        print(line)
        f.write(line + "\n")

print(f"✅ Generación de datasets completa y verificada. Checksums guardados en {checksums_file}")
