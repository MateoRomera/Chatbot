#!/usr/bin/env python3
"""
Script de verificación del sistema para SDF Assistant
"""

import os
import sys
import subprocess
import requests
import importlib
from pathlib import Path

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detectado")
        print("   Se requiere Python 3.8 o superior")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def check_dependencies():
    """Verifica las dependencias instaladas"""
    print("\n📦 Verificando dependencias...")
    
    required_packages = [
        "streamlit",
        "langchain_ollama", 
        "pandas",
        "PyPDF2",
        "docx",
        "chardet",
        "dotenv",
        "requests",
        "numpy",
        "openpyxl",
        "xlrd",
        "psutil"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "docx":
                importlib.import_module("docx")
            elif package == "dotenv":
                importlib.import_module("dotenv")
            elif package == "PyPDF2":
                importlib.import_module("PyPDF2")
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - FALTANTE")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Paquetes faltantes: {', '.join(missing_packages)}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def check_ollama():
    """Verifica Ollama"""
    print("\n🤖 Verificando Ollama...")
    
    # Verificar si ollama está instalado
    try:
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Ollama instalado: {result.stdout.strip()}")
        else:
            print("❌ Ollama no está instalado correctamente")
            return False
    except FileNotFoundError:
        print("❌ Ollama no está instalado")
        print("💡 Descarga desde: https://ollama.ai")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Timeout verificando Ollama")
        return False
    
    # Verificar si está ejecutándose
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama está ejecutándose")
            return True
        else:
            print(f"❌ Ollama responde con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Ollama no está ejecutándose")
        print("💡 Ejecuta: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error verificando Ollama: {e}")
        return False

def check_model():
    """Verifica el modelo configurado"""
    print("\n🧠 Verificando modelo...")
    
    try:
        from config import Config
        model_name = Config.OLLAMA_MODEL
        print(f"📋 Modelo configurado: {model_name}")
    except ImportError:
        print("❌ No se pudo importar config.py")
        return False
    except Exception as e:
        print(f"❌ Error leyendo configuración: {e}")
        return False
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            
            if model_name in model_names:
                print(f"✅ Modelo {model_name} encontrado")
                return True
            else:
                print(f"❌ Modelo {model_name} no encontrado")
                print("📋 Modelos disponibles:")
                for model in models:
                    print(f"   - {model.get('name', 'N/A')}")
                print(f"\n💡 Instala el modelo: ollama pull {model_name}")
                return False
        else:
            print("❌ No se pudo verificar modelos")
            return False
    except Exception as e:
        print(f"❌ Error verificando modelo: {e}")
        return False

def check_folders():
    """Verifica las carpetas necesarias"""
    print("\n📁 Verificando carpetas...")
    
    try:
        from config import Config
        folders = [Config.CONTEXT_FOLDER, Config.VECTOR_DB_PATH]
    except ImportError:
        folders = ["contexto", "vector_db"]
    
    for folder in folders:
        folder_path = Path(folder)
        if folder_path.exists():
            print(f"✅ {folder}/")
        else:
            print(f"❌ {folder}/ - NO EXISTE")
            try:
                folder_path.mkdir()
                print(f"   📁 Carpeta {folder} creada")
            except Exception as e:
                print(f"   ❌ Error creando carpeta: {e}")

def check_config():
    """Verifica la configuración"""
    print("\n⚙️ Verificando configuración...")
    
    try:
        from config import Config
        print(f"✅ Configuración cargada correctamente")
        print(f"   - Ollama URL: {Config.OLLAMA_BASE_URL}")
        print(f"   - Modelo: {Config.OLLAMA_MODEL}")
        print(f"   - Puerto: {Config.STREAMLIT_PORT}")
        print(f"   - Host: {Config.STREAMLIT_HOST}")
        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_model_response():
    """Prueba una respuesta del modelo"""
    print("\n🧪 Probando respuesta del modelo...")
    
    try:
        from config import Config
        
        payload = {
            "model": Config.OLLAMA_MODEL,
            "prompt": "Responde 'OK' si funcionas correctamente.",
            "stream": False
        }
        
        response = requests.post(
            f"{Config.OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Modelo responde correctamente")
            print(f"   Respuesta: {result.get('response', 'N/A')[:50]}...")
            return True
        else:
            print(f"❌ Error en respuesta: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error probando modelo: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🔍 Verificación del Sistema - SDF Assistant")
    print("=" * 50)
    
    checks = [
        ("Python", check_python_version),
        ("Dependencias", check_dependencies),
        ("Ollama", check_ollama),
        ("Modelo", check_model),
        ("Carpetas", check_folders),
        ("Configuración", check_config),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error en verificación {name}: {e}")
            results.append((name, False))
    
    # Prueba del modelo solo si todo lo demás está bien
    if all(result for _, result in results):
        try:
            model_result = test_model_response()
            results.append(("Respuesta del Modelo", model_result))
        except Exception as e:
            print(f"❌ Error probando modelo: {e}")
            results.append(("Respuesta del Modelo", False))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "✅ OK" if result else "❌ PROBLEMA"
        print(f"{name:<20} {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 ¡Todo está funcionando correctamente!")
        print("🚀 Puedes ejecutar SDF Assistant sin problemas")
        print("\n💡 Para iniciar:")
        print("   python run_sdf.py")
        print("   o")
        print("   iniciar_sdf.bat")
    else:
        print("⚠️ Se encontraron problemas:")
        print("💡 Revisa los errores arriba y soluciona los problemas")
        print("💡 Ejecuta: python setup_sdf.py para instalación automática")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
