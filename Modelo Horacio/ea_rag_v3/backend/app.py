from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.chat_engine import ChatEngine
from backend.config import POSTGRES_CONN
import psycopg2
import psycopg2.extras
import logging, os

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/backend.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = FastAPI(title="EA RAG v3 API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_engine = ChatEngine(conn_str=POSTGRES_CONN)

@app.on_event("startup")
async def startup_event():
    try:
        chat_engine.load_data(from_postgres=True)
        logging.info("✅ Backend iniciado y datos cargados")
    except Exception as e:
        logging.error(f"❌ Error al iniciar: {e}")

# --- Healthcheck ---
@app.get("/api/health")
def health():
    return {"success": True, "data": {"status": "healthy"}}

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

# --- Structured Query ---
@app.get("/api/structured_query")
def structured_query(fuerza: str = None, provincia: str = None, especialidad: str = None):
    try:
        conn = psycopg2.connect(POSTGRES_CONN)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "SELECT id, nombre_completo, fuerza, provincia, especialidad FROM personal WHERE 1=1"
        params = []
        if fuerza:
            query += " AND fuerza = %s"
            params.append(fuerza)
        if provincia:
            query += " AND provincia = %s"
            params.append(provincia)
        if especialidad:
            query += " AND especialidad = %s"
            params.append(especialidad)
        query += " LIMIT 50"

        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close(); conn.close()

        results = [dict(row) for row in rows]
        logging.info(f"[STRUCTURED] filtros={params} → {len(results)} resultados")

        return {"success": True, "data": {"filters": {"fuerza": fuerza, "provincia": provincia, "especialidad": especialidad}, "results": results}}
    except Exception as e:
        logging.error(f"❌ Error en /api/structured_query: {e}")
        return {"success": False, "error": str(e)}
