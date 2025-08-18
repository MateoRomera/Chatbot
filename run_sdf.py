#!/usr/bin/env python3
"""
Script de ejecución para SDF Assistant
"""

import sys
import subprocess
import requests
from pathlib import Path
from config import Config

def check_ollama():
    """Verifica que Ollama esté ejecutándose"""
    try:
        response = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_model():
    """Verifica que el modelo configurado esté disponible"""
    try:
        response = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            return Config.OLLAMA_MODEL in model_names
        return False
    except:
        return False

def check_dependencies():
    """Verifica las dependencias básicas"""
    try:
        import streamlit
        import langchain_ollama
        import pandas
        return True
    except ImportError:
        return False

def create_context_folder():
    """Crea la carpeta de contexto si no existe"""
    context_folder = Path(Config.CONTEXT_FOLDER)
    if not context_folder.exists():
        context_folder.mkdir()
        print(f"📁 Carpeta '{Config.CONTEXT_FOLDER}' creada")

def main():
    """Función principal simplificada"""
    print("🤖 SDF Assistant - Iniciando...")
    print(f"🔧 Configuración:")
    print(f"   - Ollama URL: {Config.OLLAMA_BASE_URL}")
    print(f"   - Modelo: {Config.OLLAMA_MODEL}")
    print(f"   - Puerto: {Config.STREAMLIT_PORT}")
    print(f"   - Host: {Config.STREAMLIT_HOST}")
    
    # Verificaciones básicas
    if not check_ollama():
        print("❌ Ollama no está ejecutándose")
        print(f"💡 Ejecuta: ollama serve")
        print(f"💡 O configura OLLAMA_BASE_URL en variables de entorno")
        return
    
    if not check_model():
        print(f"❌ Modelo {Config.OLLAMA_MODEL} no encontrado")
        print(f"💡 Ejecuta: ollama pull {Config.OLLAMA_MODEL}")
        print(f"💡 O configura OLLAMA_MODEL en variables de entorno")
        return
    
    if not check_dependencies():
        print("❌ Dependencias no instaladas")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return
    
    # Crear carpeta de contexto
    create_context_folder()
    
    # Iniciar aplicación
    print("🚀 Iniciando SDF Assistant...")
    print(f"🌐 URL: http://{Config.STREAMLIT_HOST}:{Config.STREAMLIT_PORT}")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_sdf.py",
            "--server.port", str(Config.STREAMLIT_PORT),
            "--server.address", Config.STREAMLIT_HOST
        ])
    except KeyboardInterrupt:
        print("\n👋 SDF Assistant cerrado")

if __name__ == "__main__":
    main()
