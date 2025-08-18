#!/usr/bin/env python3
"""
Script de inicio rápido para NachoGPT
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Imprime el banner de bienvenida"""
    print("""
🤖 NACHOGPT - ASISTENTE IA AVANZADO
=====================================
¡Bienvenido! Este script te ayudará a configurar NachoGPT rápidamente.
""")

def check_requirements():
    """Verifica los requisitos básicos"""
    print("🔍 Verificando requisitos...")
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    
    print("✅ Python detectado")
    return True

def install_dependencies():
    """Instala las dependencias"""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ Dependencias instaladas")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error instalando dependencias")
        return False

def create_folders():
    """Crea las carpetas necesarias"""
    print("\n📁 Creando carpetas...")
    
    folders = ["contexto", "vector_db"]
    for folder in folders:
        folder_path = Path(folder)
        if not folder_path.exists():
            folder_path.mkdir()
            print(f"✅ Carpeta '{folder}' creada")
        else:
            print(f"✅ Carpeta '{folder}' ya existe")

def check_ollama():
    """Verifica Ollama"""
    print("\n🤖 Verificando Ollama...")
    
    try:
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ollama detectado")
            return True
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

def setup_model():
    """Configura el modelo"""
    print("\n🧠 Configurando modelo...")
    
    try:
        from config import Config
        model_name = Config.OLLAMA_MODEL
    except ImportError:
        model_name = "gpt-oss:20b"
    
    print(f"📋 Modelo a instalar: {model_name}")
    
    response = input("¿Deseas instalar el modelo ahora? (s/n): ")
    if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        print("📥 Instalando modelo (esto puede tomar varios minutos)...")
        try:
            subprocess.run(["ollama", "pull", model_name], check=True)
            print("✅ Modelo instalado correctamente")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error instalando modelo")
            return False
    else:
        print("⚠️ Modelo no instalado. Puedes instalarlo manualmente con:")
        print(f"   ollama pull {model_name}")
        return True

def create_env_file():
    """Crea archivo .env básico"""
    print("\n📝 Creando archivo de configuración...")
    
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, "w", encoding="utf-8") as f:
            f.write("# Configuración básica de NachoGPT\n")
            f.write("OLLAMA_MODEL=gpt-oss:20b\n")
            f.write("STREAMLIT_PORT=8501\n")
            f.write("STREAMLIT_HOST=localhost\n")
        print("✅ Archivo .env creado")
    else:
        print("✅ Archivo .env ya existe")

def show_next_steps():
    """Muestra los próximos pasos"""
    print("\n" + "=" * 50)
    print("🎉 ¡Configuración completada!")
    print("=" * 50)
    
    print("\n📋 Próximos pasos:")
    print("1. 📁 Coloca tus documentos en la carpeta 'contexto/'")
    print("2. 🚀 Ejecuta: python run_nachogpt.py")
    print("3. 🌐 Abre tu navegador en: http://localhost:8501")
    print("4. 💬 ¡Comienza a hacer preguntas!")
    
    print("\n📚 Ejemplos de preguntas:")
    print("   - '¿Cuántos empleados hay en el Excel?'")
    print("   - '¿Qué políticas contiene el PDF?'")
    print("   - 'Analiza los datos de ventas'")
    
    print("\n🔧 Si tienes problemas:")
    print("   - Ejecuta: python check_system.py")
    print("   - Ejecuta: python setup_nachogpt.py")
    
    print("\n💡 Comandos útiles:")
    print("   python run_nachogpt.py     # Iniciar NachoGPT")
    print("   python check_system.py     # Verificar sistema")
    print("   iniciar_nachogpt.bat       # Script Windows")

def main():
    """Función principal"""
    print_banner()
    
    if not check_requirements():
        print("❌ No se cumplen los requisitos mínimos")
        return False
    
    if not install_dependencies():
        print("❌ Error en la instalación")
        return False
    
    create_folders()
    
    if not check_ollama():
        print("⚠️ Ollama no está disponible")
        print("💡 Instala Ollama desde https://ollama.ai")
        print("💡 Luego ejecuta: ollama serve")
    
    setup_model()
    create_env_file()
    show_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ La configuración no se completó")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Configuración cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
