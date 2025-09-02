import pandas as pd
import os, glob, sqlite3, json

DATA_DIR = os.getenv("DEFENSA_DATA_DIR", "backend/data")

def load_all_data():
    """Carga todos los datasets en un único DataFrame coherente."""
    frames = []

    # CSV
    for f in glob.glob(f"{DATA_DIR}/*.csv"):
        try:
            df = pd.read_csv(f)
            frames.append(df)
        except Exception:
            pass

    # JSON
    for f in glob.glob(f"{DATA_DIR}/*.json"):
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, list):
                frames.append(pd.DataFrame(data))
        except Exception:
            pass

    # XLSX
    for f in glob.glob(f"{DATA_DIR}/*.xlsx"):
        try:
            frames.append(pd.read_excel(f))
        except Exception:
            pass

    # SQLite
    for f in glob.glob(f"{DATA_DIR}/*.sqlite"):
        try:
            conn = sqlite3.connect(f)
            frames.append(pd.read_sql("select * from personal", conn))
            conn.close()
        except Exception:
            pass

    if not frames:
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)

    # Normalizamos columnas
    for col in ["fuerza","provincia","especialidad","formacion"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()

    return df

DATAFRAME = load_all_data()

def query_with_filters(fuerza="", provincia="", especialidad="", formacion=""):
    if DATAFRAME.empty:
        return []

    df = DATAFRAME.copy()
    if fuerza:
        df = df[df.get("fuerza","").str.lower() == fuerza.lower()]
    if provincia:
        df = df[df.get("provincia","").str.lower() == provincia.lower()]
    if especialidad:
        df = df[df.get("especialidad","").str.lower() == especialidad.lower()]
    if formacion:
        df = df[df.get("formacion","").str.lower() == formacion.lower()]

    return df.to_dict(orient="records")
