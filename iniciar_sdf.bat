@echo off
chcp 65001 >nul
title SDF Assistant - Asistente IA

echo.
echo ========================================
echo    🤖 SDF Assistant - Asistente IA
echo ========================================
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
echo 🔍 Verificando Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Ollama no está ejecutándose
    echo Por favor, inicia Ollama y vuelve a intentar
    echo Puedes descargarlo desde: https://ollama.ai
    pause
    exit /b 1
)

echo ✅ Ollama está ejecutándose

:: Verificar si el modelo está disponible (usando configuración)
echo 🔍 Verificando modelo...
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
        echo ❌ El modelo es necesario para ejecutar SDF Assistant
        pause
        exit /b 1
    )
) else (
    echo ✅ Modelo %MODEL_NAME% encontrado
)

:: Instalar dependencias si es necesario
echo 🔍 Verificando dependencias...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
    echo ✅ Dependencias instaladas
) else (
    echo ✅ Dependencias verificadas
)

:: Crear carpeta de contexto si no existe
if not exist "contexto" (
    echo 📁 Creando carpeta de contexto...
    mkdir contexto
)

echo.
echo ✅ Todo listo para ejecutar SDF Assistant!
echo 🚀 Iniciando aplicación...
echo.
echo 📝 Instrucciones:
echo   1. La aplicación se abrirá en tu navegador
echo   2. Coloca tus documentos en la carpeta 'contexto'
echo   3. Haz preguntas sobre tus documentos
echo   4. Presiona Ctrl+C para cerrar
echo.
echo ========================================
echo.

:: Ejecutar la aplicación
python run_sdf.py

echo.
echo 👋 SDF Assistant cerrado
pause
