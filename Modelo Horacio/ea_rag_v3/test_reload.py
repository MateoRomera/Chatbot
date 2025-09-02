#!/usr/bin/env python3
"""
test_reload.py
--------------
Script para probar la funcionalidad de recarga de datos del chatbot.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"


def test_reload_functionality():
    """Prueba la funcionalidad de recarga de datos"""

    print("🧪 Probando funcionalidad de recarga de datos...")

    # 1. Obtener archivos de datos actuales
    print("\n1. Obteniendo archivos de datos actuales...")
    try:
        response = requests.get(f"{BASE_URL}/api/data_files")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                files = data["data"]["files"]
                print(f"✅ Archivos cargados: {len(files)}")
                for file in files:
                    print(
                        f"   - {file['name']} ({file['type']}) - {file['size']} bytes")
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    # 2. Probar recarga de datos
    print("\n2. Probando recarga de datos...")
    try:
        response = requests.post(f"{BASE_URL}/api/reload_data")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                result = data["data"]
                print(f"✅ Recarga exitosa: {result['message']}")
                print(f"   Archivos: {', '.join(result['files'])}")
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    # 3. Verificar archivos después de la recarga
    print("\n3. Verificando archivos después de la recarga...")
    try:
        response = requests.get(f"{BASE_URL}/api/data_files")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                files = data["data"]["files"]
                print(f"✅ Archivos después de recarga: {len(files)}")
                for file in files:
                    print(
                        f"   - {file['name']} ({file['type']}) - {file['size']} bytes")
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    # 4. Probar una consulta simple
    print("\n4. Probando consulta simple...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/ask?query=personal del ejército")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                print(
                    f"✅ Consulta exitosa: {data['data']['response'][:100]}...")
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    print("\n🎉 Pruebas completadas!")


if __name__ == "__main__":
    test_reload_functionality()
