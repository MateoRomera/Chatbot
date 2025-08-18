#!/usr/bin/env python3
"""
Script de instalación y configuración para SDF Assistant
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def check_python_version():
    """Verifica la versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 o superior es requerido")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def install_dependencies():
    """Instala las dependencias necesarias"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def check_ollama():
    """Verifica si Ollama está instalado y ejecutándose"""
    print("🔍 Verificando Ollama...")
    
    # Verificar si ollama está en PATH
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama instalado: {result.stdout.strip()}")
        else:
            print("❌ Ollama no está instalado")
            print("💡 Descarga desde: https://ollama.ai")
            return False
    except FileNotFoundError:
        print("❌ Ollama no está instalado")
        print("💡 Descarga desde: https://ollama.ai")
        return False
    
    # Verificar si está ejecutándose
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama está ejecutándose")
            return True
        else:
            print("❌ Ollama no responde correctamente")
            return False
    except:
        print("❌ Ollama no está ejecutándose")
        print("💡 Ejecuta: ollama serve")
        return False

def setup_model():
    """Configura el modelo de IA"""
    from config import Config
    print(f"🤖 Configurando modelo: {Config.OLLAMA_MODEL}")
    
    try:
        response = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            
            if Config.OLLAMA_MODEL in model_names:
                print(f"✅ Modelo {Config.OLLAMA_MODEL} ya está instalado")
                return True
            else:
                print(f"📥 Instalando modelo {Config.OLLAMA_MODEL}...")
                print("⚠️ Esto puede tomar varios minutos...")
                
                result = subprocess.run([
                    "ollama", "pull", Config.OLLAMA_MODEL
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Modelo {Config.OLLAMA_MODEL} instalado correctamente")
                    return True
                else:
                    print(f"❌ Error instalando modelo: {result.stderr}")
                    return False
        else:
            print("❌ No se pudo verificar modelos")
            return False
    except Exception as e:
        print(f"❌ Error configurando modelo: {e}")
        return False

def create_folders():
    """Crea las carpetas necesarias"""
    from config import Config
    folders = [Config.CONTEXT_FOLDER, Config.VECTOR_DB_PATH]
    
    for folder in folders:
        folder_path = Path(folder)
        if not folder_path.exists():
            folder_path.mkdir()
            print(f"📁 Carpeta '{folder}' creada")
        else:
            print(f"✅ Carpeta '{folder}' ya existe")

def create_env_file():
    """Crea archivo .env si no existe"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creando archivo .env...")
        with open(env_file, "w", encoding="utf-8") as f:
            f.write("# Configuración de SDF Assistant\n")
            f.write("# Copia las variables que necesites desde env_example.txt\n")
        print("✅ Archivo .env creado")
        print("💡 Edita .env para personalizar la configuración")
    else:
        print("✅ Archivo .env ya existe")

def main():
    """Función principal de instalación"""
    print("🤖 Instalador de SDF Assistant")
    print("=" * 40)
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Instalar dependencias
    if not install_dependencies():
        return False
    
    # Verificar Ollama
    if not check_ollama():
        return False
    
    # Configurar modelo
    if not setup_model():
        return False
    
    # Crear carpetas
    create_folders()
    
    # Crear archivo .env
    create_env_file()
    
    print("\n" + "=" * 40)
    print("🎉 ¡SDF Assistant instalado correctamente!")
    print("\n📋 Próximos pasos:")
    print("1. Edita el archivo .env si necesitas personalizar la configuración")
    print("2. Coloca tus documentos en la carpeta 'contexto'")
    print("3. Ejecuta: python run_sdf.py")
    print("4. O ejecuta: iniciar_sdf.bat (Windows)")
    print("\n🌐 La aplicación estará disponible en: http://localhost:8502")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ La instalación no se completó correctamente")
        sys.exit(1)
