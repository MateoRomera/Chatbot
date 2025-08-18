#!/usr/bin/env python3
"""
Script simplificado para ejecutar NachoGPT
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def check_ollama():
    """Verifica que Ollama esté ejecutándose"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_model():
    """Verifica que el modelo gpt-oss:20b esté disponible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            return "gpt-oss:20b" in model_names
        return False
    except:
        return False

def create_context_folder():
    """Crea la carpeta de contexto si no existe"""
    context_folder = Path("contexto")
    if not context_folder.exists():
        context_folder.mkdir()
        print("📁 Carpeta 'contexto' creada")

def main():
    """Función principal simplificada"""
    print("🤖 NachoGPT - Iniciando...")
    
    # Verificaciones básicas
    if not check_ollama():
        print("❌ Ollama no está ejecutándose")
        print("💡 Ejecuta: ollama serve")
        return
    
    if not check_model():
        print("❌ Modelo gpt-oss:20b no encontrado")
        print("💡 Ejecuta: ollama pull gpt-oss:20b")
        return
    
    # Crear carpeta de contexto
    create_context_folder()
    
    # Iniciar aplicación
    print("🚀 Iniciando NachoGPT...")
    print("🌐 URL: http://localhost:8501")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_nachogpt.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 NachoGPT cerrado")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
