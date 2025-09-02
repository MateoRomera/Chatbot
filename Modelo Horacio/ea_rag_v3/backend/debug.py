import psycopg2
from backend.config import POSTGRES_CONN

def check_connection():
    info = {"conn_str": POSTGRES_CONN, "user": None, "db": None}
    try:
        conn = psycopg2.connect(POSTGRES_CONN)
        cur = conn.cursor()
        cur.execute("SELECT current_user, current_database();")
        row = cur.fetchone()
        info["user"] = row[0]
        info["db"] = row[1]
        cur.close(); conn.close()
        info["status"] = "ok"
    except Exception as e:
        info["status"] = f"error: {e}"
    return info
