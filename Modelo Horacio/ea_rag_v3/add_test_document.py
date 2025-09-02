#!/usr/bin/env python3
"""
add_test_document.py
--------------------
Script para agregar un documento de prueba y verificar que el chatbot lo detecte.
"""

import json
import pandas as pd
import requests
import time
from pathlib import Path

# Configuración
DATA_DIR = Path("data")
BASE_URL = "http://localhost:8000"


def create_test_document():
    """Crea un documento de prueba"""

    # Crear datos de prueba
    test_data = [
        {
            "Nombre completo": "Juan Carlos Test",
            "Fuerza": "Ejército",
            "Provincia": "Buenos Aires",
            "Especialidad": "Ingeniero",
            "Grado o Rango": "Teniente",
            "DNI": "12345678"
        },
        {
            "Nombre completo": "María Elena Prueba",
            "Fuerza": "Armada",
            "Provincia": "Córdoba",
            "Especialidad": "Médico",
            "Grado o Rango": "Capitán",
            "DNI": "87654321"
        }
    ]

    # Crear archivo JSON de prueba
    test_file = DATA_DIR / "personal_test.json"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Documento de prueba creado: {test_file}")
    return test_file


def test_document_detection():
    """Prueba la detección del nuevo documento"""

    print("\n🧪 Probando detección del nuevo documento...")

    # 1. Obtener archivos antes de agregar el documento
    print("\n1. Archivos antes de agregar documento de prueba:")
    try:
        response = requests.get(f"{BASE_URL}/api/data_files")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                files = data["data"]["files"]
                print(f"   Archivos cargados: {len(files)}")
                for file in files:
                    print(f"   - {file['name']}")
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    # 2. Crear documento de prueba
    print("\n2. Creando documento de prueba...")
    test_file = create_test_document()

    # 3. Recargar datos
    print("\n3. Recargando datos...")
    try:
        response = requests.post(f"{BASE_URL}/api/reload_data")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                result = data["data"]
                print(f"✅ Recarga exitosa: {result['message']}")
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    # 4. Verificar que el nuevo documento fue detectado
    print("\n4. Verificando detección del nuevo documento:")
    try:
        response = requests.get(f"{BASE_URL}/api/data_files")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                files = data["data"]["files"]
                print(f"   Archivos después de recarga: {len(files)}")

                # Buscar el archivo de prueba
                test_found = False
                for file in files:
                    print(f"   - {file['name']}")
                    if file['name'] == "personal_test.json":
                        test_found = True
                        print(f"   ✅ ¡Archivo de prueba detectado!")

                if not test_found:
                    print("   ❌ Archivo de prueba no detectado")
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    # 5. Probar consulta con el nuevo documento
    print("\n5. Probando consulta con nuevo documento:")
    try:
        response = requests.get(f"{BASE_URL}/api/ask?query=Juan Carlos Test")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                print(f"✅ Consulta exitosa: {data['data']['response']}")
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return

    print("\n🎉 Prueba completada!")


def cleanup_test_document():
    """Limpia el documento de prueba"""
    test_file = DATA_DIR / "personal_test.json"
    if test_file.exists():
        test_file.unlink()
        print(f"🗑️ Documento de prueba eliminado: {test_file}")


if __name__ == "__main__":
    try:
        test_document_detection()
    finally:
        # Preguntar si quiere limpiar
        response = input("\n¿Desea eliminar el documento de prueba? (s/n): ")
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            cleanup_test_document()
