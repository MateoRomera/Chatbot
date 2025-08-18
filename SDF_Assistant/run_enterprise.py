#!/usr/bin/env python3
"""
SDF Assistant - Enterprise Edition Launcher
Script de inicio para la versión enterprise
"""

import sys
import subprocess
import requests
import time
from pathlib import Path
from config import Config

def print_enterprise_banner():
    """Imprimir banner enterprise"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    SDF ASSISTANT ENTERPRISE                  ║
║                Document Intelligence Platform                 ║
║                        Version 2.0                          ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_enterprise_requirements():
    """Verificar requisitos enterprise"""
    print("🔍 Verificando requisitos enterprise...")
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requerido")
        return False
    
    # Verificar dependencias enterprise
    enterprise_packages = [
        "streamlit", "langchain_ollama", "pandas", "plotly", 
        "psutil", "requests", "numpy"
    ]
    
    missing_packages = []
    for package in enterprise_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Paquetes faltantes: {', '.join(missing_packages)}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Requisitos enterprise verificados")
    return True

def check_ollama_enterprise():
    """Verificar Ollama para enterprise"""
    print("🤖 Verificando Ollama Enterprise...")
    
    try:
        response = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            
            if Config.OLLAMA_MODEL in model_names:
                print(f"✅ Modelo enterprise {Config.OLLAMA_MODEL} disponible")
                return True
            else:
                print(f"⚠️ Modelo {Config.OLLAMA_MODEL} no encontrado")
                print("💡 Modelos disponibles:")
                for model in models:
                    print(f"   - {model.get('name', 'N/A')}")
                return False
        else:
            print("❌ Ollama no responde correctamente")
            return False
    except Exception as e:
        print(f"❌ Error verificando Ollama: {e}")
        return False

def setup_enterprise_environment():
    """Configurar entorno enterprise"""
    print("⚙️ Configurando entorno enterprise...")
    
    # Crear directorios enterprise
    enterprise_dirs = ["logs", "backups", "exports", "temp"]
    for dir_name in enterprise_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir()
            print(f"📁 Directorio {dir_name} creado")
    
    # Verificar configuración
    print(f"🔧 Configuración Enterprise:")
    print(f"   - Modelo: {Config.OLLAMA_MODEL}")
    print(f"   - Puerto: {Config.STREAMLIT_PORT}")
    print(f"   - Host: {Config.STREAMLIT_HOST}")
    print(f"   - Contexto: {Config.MAX_CONTEXT_LENGTH} tokens")
    print(f"   - Workers: {Config.MAX_WORKERS}")

def start_enterprise_monitoring():
    """Iniciar monitoreo enterprise"""
    print("📊 Iniciando monitoreo enterprise...")
    
    try:
        from enterprise_monitor import enterprise_monitor
        enterprise_monitor.start_monitoring(interval=30)
        print("✅ Monitoreo enterprise iniciado")
        return True
    except Exception as e:
        print(f"⚠️ Error iniciando monitoreo: {e}")
        return False

def launch_enterprise_app():
    """Lanzar aplicación enterprise"""
    print("🚀 Lanzando SDF Assistant Enterprise...")
    
    try:
        # Lanzar aplicación principal
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_sdf.py",
            "--server.port", str(Config.STREAMLIT_PORT),
            "--server.address", Config.STREAMLIT_HOST,
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 SDF Assistant Enterprise cerrado")
    except Exception as e:
        print(f"❌ Error lanzando aplicación: {e}")

def launch_admin_panel():
    """Lanzar panel de administración"""
    print("🔧 Lanzando panel de administración...")
    
    try:
        admin_port = Config.STREAMLIT_PORT + 1
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "admin_panel.py",
            "--server.port", str(admin_port),
            "--server.address", Config.STREAMLIT_HOST,
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Panel de administración cerrado")
    except Exception as e:
        print(f"❌ Error lanzando panel admin: {e}")

def main():
    """Función principal enterprise"""
    print_enterprise_banner()
    
    # Verificar requisitos
    if not check_enterprise_requirements():
        print("❌ Requisitos enterprise no cumplidos")
        sys.exit(1)
    
    # Verificar Ollama
    if not check_ollama_enterprise():
        print("❌ Ollama enterprise no disponible")
        sys.exit(1)
    
    # Configurar entorno
    setup_enterprise_environment()
    
    # Iniciar monitoreo
    monitoring_started = start_enterprise_monitoring()
    
    print("\n" + "=" * 60)
    print("🎯 SDF ASSISTANT ENTERPRISE - OPCIONES DE INICIO")
    print("=" * 60)
    print("1. 🚀 Aplicación Principal (Chat)")
    print("2. 🔧 Panel de Administración")
    print("3. 📊 Solo Monitoreo")
    print("4. ❌ Salir")
    print("=" * 60)
    
    while True:
        try:
            choice = input("\nSelecciona una opción (1-4): ").strip()
            
            if choice == "1":
                print("\n🌐 Iniciando aplicación principal...")
                print(f"📱 URL: http://{Config.STREAMLIT_HOST}:{Config.STREAMLIT_PORT}")
                launch_enterprise_app()
                break
                
            elif choice == "2":
                print("\n🔧 Iniciando panel de administración...")
                admin_port = Config.STREAMLIT_PORT + 1
                print(f"📊 URL: http://{Config.STREAMLIT_HOST}:{admin_port}")
                launch_admin_panel()
                break
                
            elif choice == "3":
                print("\n📊 Ejecutando solo monitoreo enterprise...")
                print("💡 Presiona Ctrl+C para detener")
                try:
                    while True:
                        time.sleep(10)
                        # Mostrar métricas cada 10 segundos
                        from enterprise_monitor import enterprise_monitor
                        health_report = enterprise_monitor.get_system_health_report()
                        health_score = health_report.get("health_score", 0)
                        print(f"📊 Health Score: {health_score}%")
                except KeyboardInterrupt:
                    print("\n👋 Monitoreo detenido")
                break
                
            elif choice == "4":
                print("👋 SDF Assistant Enterprise cerrado")
                break
                
            else:
                print("❌ Opción inválida. Selecciona 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 SDF Assistant Enterprise cerrado")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break
    
    # Detener monitoreo si estaba activo
    if monitoring_started:
        try:
            from enterprise_monitor import enterprise_monitor
            enterprise_monitor.stop_monitoring()
            print("✅ Monitoreo enterprise detenido")
        except:
            pass

if __name__ == "__main__":
    main()
