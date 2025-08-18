@echo off
chcp 65001 >nul
title SDF Assistant Enterprise - Document Intelligence Platform

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    SDF ASSISTANT ENTERPRISE                  ║
echo ║                Document Intelligence Platform                 ║
echo ║                        Version 2.0                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo Por favor, instala Python desde https://python.org
    pause
    exit /b 1
)

:: Verificar si Ollama está ejecutándose
echo 🔍 Verificando Ollama Enterprise...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Ollama no está ejecutándose
    echo Por favor, inicia Ollama y vuelve a intentar
    echo Puedes descargarlo desde: https://ollama.ai
    pause
    exit /b 1
)

echo ✅ Ollama está ejecutándose

:: Verificar si el modelo está disponible
echo 🔍 Verificando modelo enterprise...
python -c "from config import Config; print(f'Modelo configurado: {Config.OLLAMA_MODEL}')" 2>nul
if errorlevel 1 (
    echo ⚠️ No se pudo leer la configuración, usando modelo por defecto
    set MODEL_NAME=gpt-oss:20b
) else (
    for /f "tokens=*" %%i in ('python -c "from config import Config; print(Config.OLLAMA_MODEL)" 2^>nul') do set MODEL_NAME=%%i
)

ollama list | findstr "%MODEL_NAME%" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Modelo %MODEL_NAME% no encontrado
    echo.
    set /p install_model="¿Deseas instalarlo ahora? (s/n): "
    if /i "%install_model%"=="s" (
        echo 🔄 Instalando modelo %MODEL_NAME%...
        ollama pull %MODEL_NAME%
        if errorlevel 1 (
            echo ❌ Error instalando el modelo
            pause
            exit /b 1
        )
        echo ✅ Modelo instalado exitosamente
    ) else (
        echo ❌ El modelo es necesario para ejecutar SDF Assistant Enterprise
        pause
        exit /b 1
    )
) else (
    echo ✅ Modelo %MODEL_NAME% encontrado
)

:: Verificar dependencias enterprise
echo 🔍 Verificando dependencias enterprise...
python -c "import streamlit, plotly, psutil" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Instalando dependencias enterprise...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
    echo ✅ Dependencias enterprise instaladas
) else (
    echo ✅ Dependencias enterprise verificadas
)

:: Crear directorios enterprise
echo 📁 Configurando directorios enterprise...
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups
if not exist "exports" mkdir exports
if not exist "temp" mkdir temp
if not exist "contexto" mkdir contexto

echo.
echo ✅ SDF Assistant Enterprise configurado correctamente!
echo 🚀 Iniciando plataforma enterprise...
echo.
echo 📝 Opciones disponibles:
echo   1. 🚀 Aplicación Principal (Chat)
echo   2. 🔧 Panel de Administración
echo   3. 📊 Solo Monitoreo
echo   4. ❌ Salir
echo.
echo ========================================
echo.

:: Ejecutar la aplicación enterprise
python run_enterprise.py

echo.
echo 👋 SDF Assistant Enterprise cerrado
pause
