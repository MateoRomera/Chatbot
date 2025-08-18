@echo off
chcp 65001 >nul
title SDF Assistant - Smart Document Finder

echo.
echo ========================================
echo    🤖 SDF Assistant - Smart Document Finder
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

:: Verificar si el modelo gpt-oss:20b está disponible
echo 🔍 Verificando modelo gpt-oss:20b...
ollama list | findstr "gpt-oss:20b" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Modelo gpt-oss:20b no encontrado
    echo.
    set /p install_model="¿Deseas instalarlo ahora? (s/n): "
    if /i "%install_model%"=="s" (
        echo 🔄 Instalando modelo gpt-oss:20b...
        ollama pull gpt-oss:20b
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
    echo ✅ Modelo gpt-oss:20b encontrado
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
echo   2. Sube tus documentos en la barra lateral
echo   3. Haz preguntas sobre tus documentos
echo   4. Presiona Ctrl+C para cerrar
echo.
echo ========================================
echo.

:: Ejecutar la aplicación
python -m streamlit run app_sdf.py --server.port 8502 --server.address localhost

echo.
echo 👋 SDF Assistant cerrado
pause
