#!/usr/bin/env python3
"""
check_setup.py
--------------
Script para verificar que todo esté configurado correctamente.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python():
    """Verifica que Python esté disponible"""
    print("🐍 Verificando Python...")
    print(f"   Versión: {sys.version}")
    print(f"   Ejecutable: {sys.executable}")
    return True


def check_directory():
    """Verifica que estemos en el directorio correcto"""
    print("\n📁 Verificando directorio del proyecto...")
    current_dir = Path.cwd()
    print(f"   Directorio actual: {current_dir}")

    required_files = [
        "backend/app_sqlite.py",
        "frontend/index.html",
        "data/",
        "venv/"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"   ✅ {file_path}")

    if missing_files:
        print(f"   ❌ Archivos faltantes: {missing_files}")
        return False

    return True


def check_venv():
    """Verifica el entorno virtual"""
    print("\n🔧 Verificando entorno virtual...")

    if not Path("venv").exists():
        print("   ❌ No se encontró el entorno virtual")
        print("   💡 Ejecuta: python -m venv venv")
        return False

    activate_script = Path(
        "venv/Scripts/activate.bat") if os.name == 'nt' else Path("venv/bin/activate")
    if not activate_script.exists():
        print(
            f"   ❌ No se encontró el script de activación: {activate_script}")
        return False

    print("   ✅ Entorno virtual encontrado")
    return True


def check_dependencies():
    """Verifica las dependencias"""
    print("\n📦 Verificando dependencias...")

    required_packages = [
        "fastapi",
        "uvicorn",
        "pandas",
        "openpyxl",
        "python-dotenv"
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - No instalado")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n   💡 Instala las dependencias faltantes:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False

    return True


def check_data_files():
    """Verifica archivos de datos"""
    print("\n📊 Verificando archivos de datos...")

    data_dir = Path("data")
    if not data_dir.exists():
        print("   ❌ No se encontró el directorio 'data'")
        return False

    data_files = list(data_dir.glob("*"))
    if not data_files:
        print("   ⚠️  El directorio 'data' está vacío")
        return True

    print(f"   ✅ Encontrados {len(data_files)} archivos:")
    for file_path in data_files:
        if file_path.is_file():
            size = file_path.stat().st_size
            print(f"      - {file_path.name} ({size} bytes)")

    return True


def test_backend():
    """Prueba el backend"""
    print("\n🔌 Probando backend...")

    try:
        # Intentar importar el módulo del backend
        sys.path.insert(0, str(Path("backend")))
        import app_sqlite
        print("   ✅ Backend se puede importar correctamente")
        return True
    except Exception as e:
        print(f"   ❌ Error al importar backend: {e}")
        return False


def main():
    """Función principal"""
    print("=" * 50)
    print("    VERIFICACIÓN DE CONFIGURACIÓN")
    print("=" * 50)

    checks = [
        check_python(),
        check_directory(),
        check_venv(),
        check_dependencies(),
        check_data_files(),
        test_backend()
    ]

    print("\n" + "=" * 50)
    print("    RESUMEN")
    print("=" * 50)

    if all(checks):
        print("✅ ¡Todo está configurado correctamente!")
        print("\n🚀 Para iniciar el chatbot:")
        print("   - Windows: start_simple.bat")
        print("   - PowerShell: .\\start_simple.ps1")
        print("   - Manual: python backend\\app_sqlite.py")
    else:
        print("❌ Hay problemas de configuración que deben resolverse.")
        print("\n🔧 Pasos para solucionar:")
        print("   1. Asegúrate de estar en el directorio raíz del proyecto")
        print("   2. Crea el entorno virtual: python -m venv venv")
        print("   3. Activa el entorno virtual")
        print("   4. Instala dependencias: pip install -r requirements.txt")
        print("   5. Ejecuta este script nuevamente")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
