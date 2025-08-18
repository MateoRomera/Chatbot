#!/usr/bin/env python3
"""
Script para ejecutar el asistente SDF
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_ollama():
    """Verifica si Ollama está ejecutándose"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Ollama está ejecutándose")
            return True
        else:
            logger.error("❌ Ollama no responde correctamente")
            return False
    except Exception as e:
        logger.error(f"❌ Error conectando con Ollama: {e}")
        return False

def check_model():
    """Verifica si el modelo gpt-oss:20b está disponible"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            for model in models:
                if "gpt-oss:20b" in model.get("name", ""):
                    logger.info("✅ Modelo gpt-oss:20b encontrado")
                    return True
            
            logger.warning("⚠️ Modelo gpt-oss:20b no encontrado")
            logger.info("Modelos disponibles:")
            for model in models:
                logger.info(f"  - {model.get('name', 'N/A')}")
            return False
        else:
            logger.error("❌ No se pudo obtener la lista de modelos")
            return False
    except Exception as e:
        logger.error(f"❌ Error verificando modelos: {e}")
        return False

def install_model():
    """Instala el modelo gpt-oss:20b si no está disponible"""
    try:
        logger.info("🔄 Instalando modelo gpt-oss:20b...")
        result = subprocess.run(
            ["ollama", "pull", "gpt-oss:20b"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos
        )
        
        if result.returncode == 0:
            logger.info("✅ Modelo gpt-oss:20b instalado exitosamente")
            return True
        else:
            logger.error(f"❌ Error instalando modelo: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("❌ Timeout instalando modelo")
        return False
    except Exception as e:
        logger.error(f"❌ Error ejecutando ollama pull: {e}")
        return False

def check_dependencies():
    """Verifica las dependencias de Python"""
    required_packages = [
        "streamlit",
        "langchain-ollama",
        "pandas",
        "PyPDF2",
        "python-docx",
        "chardet",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.warning(f"⚠️ Paquetes faltantes: {', '.join(missing_packages)}")
        logger.info("Instalando dependencias...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], check=True)
            logger.info("✅ Dependencias instaladas")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Error instalando dependencias: {e}")
            return False
    else:
        logger.info("✅ Todas las dependencias están instaladas")
        return True

def create_context_folder():
    """Crea la carpeta de contexto si no existe"""
    context_folder = Path("contexto")
    if not context_folder.exists():
        context_folder.mkdir()
        logger.info("✅ Carpeta 'contexto' creada")
    else:
        logger.info("✅ Carpeta 'contexto' ya existe")

def main():
    """Función principal"""
    print("🤖 Iniciando SDF Assistant...")
    print("=" * 50)
    
    # Verificar Ollama
    if not check_ollama():
        print("\n❌ Ollama no está ejecutándose.")
        print("Por favor, inicia Ollama y vuelve a intentar.")
        print("Puedes descargarlo desde: https://ollama.ai")
        return False
    
    # Verificar modelo
    if not check_model():
        print("\n⚠️ Modelo gpt-oss:20b no encontrado.")
        response = input("¿Deseas instalarlo ahora? (s/n): ")
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            if not install_model():
                print("❌ No se pudo instalar el modelo.")
                return False
        else:
            print("❌ El modelo es necesario para ejecutar SDF Assistant.")
            return False
    
    # Verificar dependencias
    if not check_dependencies():
        print("❌ No se pudieron instalar las dependencias.")
        return False
    
    # Crear carpeta de contexto
    create_context_folder()
    
    print("\n✅ Todo listo para ejecutar SDF Assistant!")
    print("🚀 Iniciando aplicación...")
    print("=" * 50)
    
    # Ejecutar Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_sdf.py",
            "--server.port", "8502",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 SDF Assistant cerrado por el usuario")
    except Exception as e:
        logger.error(f"❌ Error ejecutando Streamlit: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
