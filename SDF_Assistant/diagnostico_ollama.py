#!/usr/bin/env python3
"""
Script de diagnóstico para Ollama y SDF Assistant
"""

import requests
import subprocess
import json
import time
import psutil

def check_ollama_status():
    """Verifica el estado de Ollama"""
    print("🔍 Verificando estado de Ollama...")
    
    try:
        # Verificar si Ollama está ejecutándose
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama está ejecutándose correctamente")
            return True
        else:
            print(f"❌ Ollama responde con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar con Ollama")
        return False
    except Exception as e:
        print(f"❌ Error verificando Ollama: {e}")
        return False

def check_model_status():
    """Verifica el estado del modelo"""
    print("\n🔍 Verificando modelo gpt-oss:20b...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            
            for model in models:
                if "gpt-oss:20b" in model.get("name", ""):
                    print(f"✅ Modelo encontrado: {model.get('name')}")
                    print(f"   Tamaño: {model.get('size', 'N/A')}")
                    print(f"   Modificado: {model.get('modified_at', 'N/A')}")
                    return True
            
            print("❌ Modelo gpt-oss:20b no encontrado")
            print("Modelos disponibles:")
            for model in models:
                print(f"   - {model.get('name', 'N/A')}")
            return False
        else:
            print(f"❌ Error obteniendo modelos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error verificando modelo: {e}")
        return False

def test_model_response():
    """Prueba una respuesta simple del modelo"""
    print("\n🧪 Probando respuesta del modelo...")
    
    try:
        payload = {
            "model": "gpt-oss:20b",
            "prompt": "Hola, responde con 'OK' si me escuchas.",
            "stream": False
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Modelo responde correctamente")
            print(f"   Respuesta: {result.get('response', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Error en respuesta del modelo: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error probando modelo: {e}")
        return False

def check_system_resources():
    """Verifica recursos del sistema"""
    print("\n💻 Verificando recursos del sistema...")
    
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"   CPU: {cpu_percent}%")
    
    # Memoria
    memory = psutil.virtual_memory()
    print(f"   Memoria: {memory.percent}% usado ({memory.available // (1024**3)} GB disponible)")
    
    # Disco
    disk = psutil.disk_usage('/')
    print(f"   Disco: {disk.percent}% usado ({disk.free // (1024**3)} GB disponible)")
    
    # Verificar si hay suficiente memoria
    if memory.available < 4 * 1024**3:  # Menos de 4GB
        print("⚠️  Advertencia: Poca memoria disponible. El modelo puede fallar.")
        return False
    
    return True

def check_ollama_process():
    """Verifica el proceso de Ollama"""
    print("\n🔍 Verificando proceso de Ollama...")
    
    ollama_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            if 'ollama' in proc.info['name'].lower():
                ollama_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if ollama_processes:
        print(f"✅ Ollama ejecutándose en {len(ollama_processes)} proceso(s)")
        for proc in ollama_processes:
            memory_mb = proc.info['memory_info'].rss // (1024**2)
            print(f"   PID {proc.info['pid']}: {memory_mb} MB")
        return True
    else:
        print("❌ No se encontraron procesos de Ollama")
        return False

def main():
    """Función principal de diagnóstico"""
    print("🤖 Diagnóstico de SDF Assistant y Ollama")
    print("=" * 50)
    
    # Verificar recursos del sistema
    resources_ok = check_system_resources()
    
    # Verificar proceso de Ollama
    process_ok = check_ollama_process()
    
    # Verificar estado de Ollama
    ollama_ok = check_ollama_status()
    
    # Verificar modelo
    model_ok = check_model_status()
    
    # Probar respuesta del modelo
    response_ok = False
    if ollama_ok and model_ok:
        response_ok = test_model_response()
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 50)
    
    print(f"💻 Recursos del sistema: {'✅ OK' if resources_ok else '❌ PROBLEMA'}")
    print(f"🔧 Proceso de Ollama: {'✅ OK' if process_ok else '❌ PROBLEMA'}")
    print(f"🌐 Servicio de Ollama: {'✅ OK' if ollama_ok else '❌ PROBLEMA'}")
    print(f"🤖 Modelo gpt-oss:20b: {'✅ OK' if model_ok else '❌ PROBLEMA'}")
    print(f"💬 Respuesta del modelo: {'✅ OK' if response_ok else '❌ PROBLEMA'}")
    
    if all([resources_ok, process_ok, ollama_ok, model_ok, response_ok]):
        print("\n🎉 ¡Todo está funcionando correctamente!")
        print("Puedes ejecutar SDF Assistant sin problemas.")
    else:
        print("\n⚠️  Se encontraron problemas:")
        if not resources_ok:
            print("   - Libera memoria o reinicia el sistema")
        if not process_ok:
            print("   - Inicia Ollama: ollama serve")
        if not ollama_ok:
            print("   - Verifica que Ollama esté ejecutándose")
        if not model_ok:
            print("   - Instala el modelo: ollama pull gpt-oss:20b")
        if not response_ok:
            print("   - Reinicia Ollama o verifica recursos del sistema")

if __name__ == "__main__":
    main()
