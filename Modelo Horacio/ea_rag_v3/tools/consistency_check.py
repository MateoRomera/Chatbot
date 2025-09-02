"""
Consistency check tool for ea_rag_v3.
Verifies that backend endpoints /health, /query, and /chat are working.
"""

import requests


def check_health():
    try:
        resp = requests.get("http://127.0.0.1:8000/health")
        print("✅ /health:", resp.json())
    except Exception as e:
        print("❌ /health failed:", str(e))


def check_query():
    try:
        params = {"fuerza": "Ejército", "provincia": "Buenos Aires"}
        resp = requests.get("http://127.0.0.1:8000/query", params=params)
        print("✅ /query:", resp.json())
    except Exception as e:
        print("❌ /query failed:", str(e))


def check_chat():
    try:
        params = {"q": "¿Cuántos candidatos hay en Buenos Aires?"}
        resp = requests.get("http://127.0.0.1:8000/chat", params=params)
        print("✅ /chat:", resp.json())
    except Exception as e:
        print("❌ /chat failed:", str(e))


if __name__ == "__main__":
    print("Running consistency checks for ea_rag_v3...")
    check_health()
    check_query()
    check_chat()
