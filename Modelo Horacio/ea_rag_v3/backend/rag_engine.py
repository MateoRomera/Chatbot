import psycopg2
import psycopg2.extras
import logging
from backend.config import POSTGRES_CONN

class RAGEngine:
    def __init__(self, conn_str=None):
        # usar siempre lo que venga del .env
        self.conn_str = conn_str or POSTGRES_CONN
        self.data = []

    def load_from_postgres(self):
        try:
            conn = psycopg2.connect(self.conn_str)
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            query = """
                SELECT id, nombre_completo, dni, fecha_nacimiento,
                       fuerza, grado_o_rango, region, provincia, destacamento,
                       formacion_universitaria, capacitacion, especialidad,
                       jefe_inmediato, telefono, correo_electronico
                FROM personal;
            """
            cur.execute(query)
            rows = cur.fetchall()
            self.data = rows
            cur.close(); conn.close()
            logging.info(f"[RAGEngine] Cargados {len(rows)} registros desde Postgres")
        except Exception as e:
            logging.error(f"❌ Error en RAGEngine.load_from_postgres: {e}")
            raise
