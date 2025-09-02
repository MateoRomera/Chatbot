from backend.rag_engine import RAGEngine
import psycopg2, psycopg2.extras
from backend.config import POSTGRES_CONN

class ChatEngine:
    def __init__(self, conn_str):
        self.rag = RAGEngine(conn_str)
        self.conn_str = conn_str

    def load_data(self, from_postgres=False):
        if from_postgres:
            self.rag.load_from_postgres()

    def ask(self, query: str):
        # Heurística muy simple: detectar filtros por palabras clave
        fuerza = None
        provincia = None
        especialidad = None

        if "ejército" in query.lower():
            fuerza = "Ejército"
        if "armada" in query.lower():
            fuerza = "Armada"
        if "fuerza aérea" in query.lower():
            fuerza = "Fuerza Aérea"

        provincias = ["Buenos Aires", "Córdoba", "Mendoza"]
        for p in provincias:
            if p.lower() in query.lower():
                provincia = p

        especialidades = ["Ingeniero", "Médico", "Infantería", "Sanidad"]
        for e in especialidades:
            if e.lower() in query.lower():
                especialidad = e

        # Si no hay filtros detectados, responder con eco
        if not (fuerza or provincia or especialidad):
            return f"Echo: {query}"

        try:
            conn = psycopg2.connect(self.conn_str)
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = "SELECT nombre_completo, fuerza, provincia, especialidad FROM personal WHERE 1=1"
            params = []
            if fuerza:
                sql += " AND fuerza = %s"
                params.append(fuerza)
            if provincia:
                sql += " AND provincia = %s"
                params.append(provincia)
            if especialidad:
                sql += " AND especialidad = %s"
                params.append(especialidad)
            sql += " LIMIT 50"

            cur.execute(sql, params)
            rows = cur.fetchall()
            cur.close(); conn.close()

            if not rows:
                return f"No encontré resultados para tu consulta ({query})."

            nombres = ", ".join([row["nombre_completo"] for row in rows])
            return f"Encontré {len(rows)} resultado(s): {nombres}"

        except Exception as e:
            return f"❌ Error al procesar la consulta: {e}"
