"""
app_sqlite.py
-------------
FastAPI application for EA RAG v3 using SQLite instead of PostgreSQL.
This version can work with the existing SQLite data files.
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import logging
import os
import json
import pandas as pd
from pathlib import Path

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/backend.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = FastAPI(title="EA RAG v3 API (SQLite)")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory
DATA_DIR = Path(__file__).parent.parent / "data"


class SQLiteChatEngine:
    """Simple chat engine using SQLite data files"""

    def __init__(self):
        self.data_files = []
        self.load_data_files()

    def load_data_files(self):
        """Load available SQLite data files"""
        sqlite_files = list(DATA_DIR.glob("*.sqlite"))
        csv_files = list(DATA_DIR.glob("*.csv"))
        json_files = list(DATA_DIR.glob("*.json"))
        xlsx_files = list(DATA_DIR.glob("*.xlsx"))

        self.data_files = sqlite_files + csv_files + json_files + xlsx_files
        logging.info(
            f"Loaded {len(self.data_files)} data files: {[f.name for f in self.data_files]}")

    def reload_data(self):
        """Reload data files from disk"""
        self.load_data_files()
        logging.info("Data files reloaded successfully")
        return {"message": f"Reloaded {len(self.data_files)} data files", "files": [f.name for f in self.data_files]}

    def query_data(self, fuerza=None, provincia=None, especialidad=None):
        """Query data from SQLite files"""
        results = []

        for file_path in self.data_files:
            try:
                if file_path.suffix == '.sqlite':
                    # Query SQLite file
                    conn = sqlite3.connect(file_path)
                    query = "SELECT nombre_completo, fuerza, provincia, especialidad FROM personal WHERE 1=1"
                    params = []

                    if fuerza:
                        query += " AND fuerza = ?"
                        params.append(fuerza)
                    if provincia:
                        query += " AND provincia = ?"
                        params.append(provincia)
                    if especialidad:
                        query += " AND especialidad = ?"
                        params.append(especialidad)

                    query += " LIMIT 50"

                    df = pd.read_sql_query(query, conn, params=params)
                    conn.close()

                    if not df.empty:
                        results.extend(df.to_dict('records'))

                elif file_path.suffix == '.csv':
                    # Query CSV file
                    df = pd.read_csv(file_path)

                    # Apply filters
                    if fuerza:
                        df = df[df['Fuerza'].str.contains(
                            fuerza, case=False, na=False)]
                    if provincia:
                        df = df[df['Provincia'].str.contains(
                            provincia, case=False, na=False)]
                    if especialidad:
                        df = df[df['Especialidad'].str.contains(
                            especialidad, case=False, na=False)]

                    df = df.head(50)

                    if not df.empty:
                        results.extend(
                            df[['Nombre completo', 'Fuerza', 'Provincia', 'Especialidad']].to_dict('records'))

                elif file_path.suffix == '.json':
                    # Query JSON file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    if isinstance(data, list):
                        df = pd.DataFrame(data)
                    elif isinstance(data, dict) and "records" in data:
                        df = pd.DataFrame(data["records"])
                    elif isinstance(data, dict):
                        df = pd.DataFrame(list(data.values()))
                    else:
                        continue

                    # Apply filters
                    if fuerza and 'Fuerza' in df.columns:
                        df = df[df['Fuerza'].str.contains(
                            fuerza, case=False, na=False)]
                    if provincia and 'Provincia' in df.columns:
                        df = df[df['Provincia'].str.contains(
                            provincia, case=False, na=False)]
                    if especialidad and 'Especialidad' in df.columns:
                        df = df[df['Especialidad'].str.contains(
                            especialidad, case=False, na=False)]

                    df = df.head(50)

                    if not df.empty:
                        # Select available columns
                        available_cols = ['Nombre completo',
                                          'Fuerza', 'Provincia', 'Especialidad']
                        cols_to_use = [
                            col for col in available_cols if col in df.columns]
                        if cols_to_use:
                            results.extend(df[cols_to_use].to_dict('records'))

                elif file_path.suffix == '.xlsx':
                    # Query XLSX file
                    df = pd.read_excel(file_path)

                    # Apply filters
                    if fuerza and 'Fuerza' in df.columns:
                        df = df[df['Fuerza'].str.contains(
                            fuerza, case=False, na=False)]
                    if provincia and 'Provincia' in df.columns:
                        df = df[df['Provincia'].str.contains(
                            provincia, case=False, na=False)]
                    if especialidad and 'Especialidad' in df.columns:
                        df = df[df['Especialidad'].str.contains(
                            especialidad, case=False, na=False)]

                    df = df.head(50)

                    if not df.empty:
                        # Select available columns
                        available_cols = ['Nombre completo',
                                          'Fuerza', 'Provincia', 'Especialidad']
                        cols_to_use = [
                            col for col in available_cols if col in df.columns]
                        if cols_to_use:
                            results.extend(df[cols_to_use].to_dict('records'))

            except Exception as e:
                logging.error(f"Error reading {file_path}: {e}")
                continue

        return results

    def ask(self, query: str):
        """Process a natural language query"""
        query_lower = query.lower()

        # Check for specific person queries
        if self._is_person_query(query_lower):
            return self._search_person(query_lower)

        # Check for general category queries
        fuerza = None
        provincia = None
        especialidad = None

        # Detect fuerza
        if "ejército" in query_lower or "ejercito" in query_lower:
            fuerza = "Ejército"
        elif "armada" in query_lower:
            fuerza = "Armada"
        elif "fuerza aérea" in query_lower or "aerea" in query_lower or "fuerza aerea" in query_lower:
            fuerza = "Fuerza Aérea"

        # Detect provincia (common provinces)
        provincias = ["Buenos Aires", "Córdoba", "Mendoza", "Santa Fe", "Salta", "Jujuy", "Tucumán", "Corrientes", "Chaco", "Formosa", "Misiones", "Entre Ríos",
                      "Santiago del Estero", "La Rioja", "Catamarca", "San Juan", "San Luis", "Neuquén", "Río Negro", "Chubut", "Santa Cruz", "Tierra del Fuego"]
        for p in provincias:
            if p.lower() in query_lower:
                provincia = p
                break

        # Detect especialidad
        especialidades = ["Ingeniero", "Médico", "Infantería", "Sanidad", "Piloto",
                          "Logística", "Artillería", "Caballería", "Comunicaciones", "Inteligencia"]
        for e in especialidades:
            if e.lower() in query_lower:
                especialidad = e
                break

        # If no filters detected, try to be helpful
        if not (fuerza or provincia or especialidad):
            return f"No pude identificar criterios específicos en tu consulta. Prueba preguntas como: 'Personal del ejército', 'Médicos en Buenos Aires', o busca por nombre específico como 'Dónde trabaja María González'."

        # Query the data
        results = self.query_data(fuerza, provincia, especialidad)

        if not results:
            return f"No encontré resultados para tu consulta ({query})."

        # Format results
        nombres = ", ".join(
            [str(r.get('nombre_completo', r.get('Nombre completo', 'N/A'))) for r in results])
        return f"Encontré {len(results)} resultado(s): {nombres}"

    def _is_person_query(self, query_lower):
        """Check if the query is asking about a specific person"""
        person_indicators = [
            "donde trabaja", "dónde trabaja", "donde esta", "dónde está",
            "cual es el id", "cuál es el id", "id de", "información de",
            "datos de", "teléfono de", "telefono de", "correo de",
            "especialidad de", "grado de", "rango de"
        ]

        # Check for direct person indicators
        if any(indicator in query_lower for indicator in person_indicators):
            return True

        # Check if query looks like a person name (has common name patterns)
        words = query_lower.split()
        if len(words) >= 2:
            # Check if it contains common first names and last names
            common_names = ["maria", "maría", "sofia", "sofía", "juan", "carlos", "ana", "luis", "pedro", "diego", "pablo", "jose", "josé",
                            "antonio", "francisco", "manuel", "rafael", "miguel", "alejandro", "fernando", "ricardo", "alberto", "eduardo", "roberto"]
            common_surnames = ["gonzalez", "gonzález", "rodriguez", "rodríguez", "martinez", "martínez", "garcia", "garcía", "lopez", "lópez", "perez", "pérez", "sanchez", "sánchez", "ramirez", "ramírez",
                               "torres", "flores", "rivera", "gomez", "gómez", "diaz", "díaz", "morales", "castro", "ortiz", "ruiz", "gutierrez", "gutiérrez", "vargas", "romero", "herrera", "medina", "jimenez", "jiménez"]

            has_first_name = any(word in common_names for word in words)
            has_surname = any(word in common_surnames for word in words)

            if has_first_name and has_surname:
                return True

        return False

    def _search_person(self, query_lower):
        """Search for a specific person by name"""
        # Extract potential names from the query
        import re

        # Look for names after common patterns
        name_patterns = [
            r"(?:donde trabaja|dónde trabaja|donde esta|dónde está|id de|información de|datos de|teléfono de|telefono de|correo de|especialidad de|grado de|rango de)\s+(.+?)(?:\s|$)",
            r"(?:cual es el id|cuál es el id)\s+de\s+(.+?)(?:\s|$)"
        ]

        potential_name = None
        for pattern in name_patterns:
            match = re.search(pattern, query_lower, re.IGNORECASE)
            if match:
                potential_name = match.group(1).strip()
                break

        if not potential_name:
            # Try to extract full name from query
            words = query_lower.split()
            common_names = ["maria", "maría", "sofia", "sofía", "juan", "carlos", "ana", "luis", "pedro", "diego", "pablo", "jose", "josé",
                            "antonio", "francisco", "manuel", "rafael", "miguel", "alejandro", "fernando", "ricardo", "alberto", "eduardo", "roberto"]
            common_surnames = ["gonzalez", "gonzález", "rodriguez", "rodríguez", "martinez", "martínez", "garcia", "garcía", "lopez", "lópez", "perez", "pérez", "sanchez", "sánchez", "ramirez", "ramírez",
                               "torres", "flores", "rivera", "gomez", "gómez", "diaz", "díaz", "morales", "castro", "ortiz", "ruiz", "gutierrez", "gutiérrez", "vargas", "romero", "herrera", "medina", "jimenez", "jiménez"]

            # Look for name patterns
            for i, word in enumerate(words):
                if word in common_names and i + 1 < len(words) and words[i + 1] in common_surnames:
                    potential_name = f"{word} {words[i + 1]}"
                    break

            # If no complete name found, try just the query as is if it looks like a name
            if not potential_name and len(words) >= 2:
                # Check if first word is a name
                if words[0] in common_names:
                    potential_name = " ".join(
                        words[:2])  # Take first two words

        if not potential_name:
            return "No pude identificar un nombre específico en tu consulta. Intenta preguntar como: 'Dónde trabaja María González' o 'Cuál es el ID de Sofia Castro'."

        # Search in data files
        results = []
        exact_matches = []
        partial_matches = []

        for file_path in self.data_files:
            try:
                if file_path.suffix == '.sqlite':
                    conn = sqlite3.connect(file_path)

                    # First try exact match
                    exact_query = "SELECT * FROM personal WHERE LOWER(nombre_completo) = ? LIMIT 5"
                    df_exact = pd.read_sql_query(exact_query, conn, params=[
                                                 potential_name.lower()])
                    if not df_exact.empty:
                        exact_matches.extend(df_exact.to_dict('records'))

                    # Then try partial match if no exact match
                    if df_exact.empty:
                        partial_query = "SELECT * FROM personal WHERE LOWER(nombre_completo) LIKE ? LIMIT 5"
                        df_partial = pd.read_sql_query(
                            partial_query, conn, params=[f'%{potential_name}%'])
                        if not df_partial.empty:
                            partial_matches.extend(
                                df_partial.to_dict('records'))

                    conn.close()

                elif file_path.suffix == '.csv':
                    df = pd.read_csv(file_path)
                    # Search in name column (try different possible column names)
                    name_columns = [
                        'Nombre completo', 'nombre_completo', 'Nombre', 'nombre', 'Name', 'name']

                    for col in name_columns:
                        if col in df.columns:
                            # First try exact match
                            exact_mask = df[col].str.lower(
                            ) == potential_name.lower()
                            exact_results = df[exact_mask].head(5)
                            if not exact_results.empty:
                                exact_matches.extend(
                                    exact_results.to_dict('records'))
                            else:
                                # Then try partial match
                                partial_mask = df[col].str.contains(
                                    potential_name, case=False, na=False)
                                partial_results = df[partial_mask].head(5)
                                if not partial_results.empty:
                                    partial_matches.extend(
                                        partial_results.to_dict('records'))
                            break

            except Exception as e:
                logging.error(f"Error searching person in {file_path}: {e}")
                continue

        # Prioritize exact matches over partial matches
        results = exact_matches if exact_matches else partial_matches

        if not results:
            return f"No encontré información sobre '{potential_name}'. Verifica que el nombre esté escrito correctamente."

        # Format detailed results for person queries
        response_parts = []
        for person in results[:3]:  # Limit to first 3 matches
            info = []

            # Get name
            name = person.get('nombre_completo', person.get(
                'Nombre completo', 'N/A'))
            info.append(f"**{name}**")

            # Get ID if requested
            if "id" in query_lower:
                person_id = person.get('id', person.get('ID', 'N/A'))
                info.append(f"ID: {person_id}")

            # Get workplace/location info
            if "donde" in query_lower or "dónde" in query_lower:
                fuerza = person.get('fuerza', person.get('Fuerza', 'N/A'))
                provincia = person.get(
                    'provincia', person.get('Provincia', 'N/A'))
                destacamento = person.get(
                    'destacamento', person.get('Destacamento', 'N/A'))
                info.append(
                    f"Trabaja en: {fuerza}, {provincia} - {destacamento}")

            # For simple name queries, provide basic info
            elif len(query_lower.split()) <= 3 and not any(keyword in query_lower for keyword in ["especialidad", "grado", "teléfono", "telefono", "correo"]):
                fuerza = person.get('fuerza', person.get('Fuerza', 'N/A'))
                provincia = person.get(
                    'provincia', person.get('Provincia', 'N/A'))
                especialidad = person.get(
                    'especialidad', person.get('Especialidad', 'N/A'))
                grado = person.get(
                    'grado_o_rango', person.get('Grado o Rango', 'N/A'))
                info.append(
                    f"{grado} - {especialidad} | {fuerza}, {provincia}")

            # Get other requested info
            if "especialidad" in query_lower:
                especialidad = person.get(
                    'especialidad', person.get('Especialidad', 'N/A'))
                info.append(f"Especialidad: {especialidad}")

            if "grado" in query_lower or "rango" in query_lower:
                grado = person.get(
                    'grado_o_rango', person.get('Grado o Rango', 'N/A'))
                info.append(f"Grado: {grado}")

            if "teléfono" in query_lower or "telefono" in query_lower:
                telefono = person.get(
                    'teléfono', person.get('Teléfono', 'N/A'))
                info.append(f"Teléfono: {telefono}")

            if "correo" in query_lower:
                correo = person.get('correo_electrónico',
                                    person.get('Correo electrónico', 'N/A'))
                info.append(f"Correo: {correo}")

            response_parts.append(" | ".join(info))

        return "\n".join(response_parts)


# Initialize chat engine
chat_engine = SQLiteChatEngine()


@app.on_event("startup")
async def startup_event():
    try:
        logging.info("✅ Backend iniciado con SQLite")
    except Exception as e:
        logging.error(f"❌ Error al iniciar: {e}")

# --- Healthcheck ---


@app.get("/api/health")
def health():
    return {"success": True, "data": {"status": "healthy", "database": "sqlite"}}

# --- Chat IA ---


@app.get("/api/ask")
def ask(query: str = Query(...)):
    try:
        response = chat_engine.ask(query)
        logging.info(f"[ASK] query='{query}' → response='{response}'")
        return {"success": True, "data": {"response": response}}
    except Exception as e:
        logging.error(f"❌ Error en /api/ask: {e}")
        return {"success": False, "error": str(e)}

# --- Reload Data ---


@app.post("/api/reload_data")
def reload_data():
    """Reload data files from disk"""
    try:
        result = chat_engine.reload_data()
        logging.info(f"[RELOAD] {result['message']}")
        return {"success": True, "data": result}
    except Exception as e:
        logging.error(f"❌ Error en /api/reload_data: {e}")
        return {"success": False, "error": str(e)}

# --- Get Data Files ---


@app.get("/api/data_files")
def get_data_files():
    """Get list of currently loaded data files"""
    try:
        files = [{"name": f.name, "type": f.suffix, "size": f.stat().st_size}
                 for f in chat_engine.data_files]
        return {"success": True, "data": {"files": files, "count": len(files)}}
    except Exception as e:
        logging.error(f"❌ Error en /api/data_files: {e}")
        return {"success": False, "error": str(e)}

# --- Structured Query ---


@app.get("/api/structured_query")
def structured_query(fuerza: str = None, provincia: str = None, especialidad: str = None):
    try:
        results = chat_engine.query_data(fuerza, provincia, especialidad)

        logging.info(
            f"[STRUCTURED] filtros={[fuerza, provincia, especialidad]} → {len(results)} resultados")

        return {
            "success": True,
            "data": {
                "filters": {"fuerza": fuerza, "provincia": provincia, "especialidad": especialidad},
                "results": results
            }
        }
    except Exception as e:
        logging.error(f"❌ Error en /api/structured_query: {e}")
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
