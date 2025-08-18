@echo off
title NachoGPT - Asistente de IA

echo ================================================
echo NACHOGPT - ASISTENTE DE IA
echo ================================================
echo Interfaz estilo ChatGPT
echo Una sola instancia en el navegador
echo Modelo: oss20B (optimizado)
echo ================================================
echo.

echo Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Instala Python desde: https://python.org
    pause
    exit /b 1
)

echo.
echo Verificando dependencias...
python -c "import streamlit, langchain_ollama, pandas, PyPDF2, docx, openpyxl, dotenv"
if errorlevel 1 (
    echo Instalando dependencias...
    pip install streamlit langchain-ollama pandas PyPDF2 python-docx openpyxl python-dotenv
)

echo.
echo Verificando Ollama...
python -c "import requests; requests.get('http://localhost:11434/api/tags', timeout=5)"
if errorlevel 1 (
    echo Ollama no esta ejecutandose
    echo Intentando iniciar Ollama...
    
    if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" (
        start /B "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" serve
        timeout /t 5 /nobreak >nul
        echo Ollama iniciado
    ) else (
        echo Ollama no encontrado. Instala desde: https://ollama.ai
        echo Luego ejecuta: ollama pull oss20B
    )
) else (
    echo Ollama esta ejecutandose
)

echo.
echo Verificando modelo oss20B...
python -c "import requests; import json; r=requests.get('http://localhost:11434/api/tags'); models=[m['name'] for m in r.json().get('models', [])]; exit(0 if 'oss20B' in models or 'oss20b' in models else 1)"
if errorlevel 1 (
    echo Modelo oss20B no encontrado
    echo Descargando modelo oss20B...
    ollama pull oss20B
)

echo.
echo Creando carpeta contexto...
if not exist "contexto" mkdir contexto

echo.
echo Iniciando NachoGPT...
echo La aplicacion estara disponible en: http://localhost:8501
echo.

timeout /t 2 /nobreak >nul
start http://localhost:8501

python run_nachogpt.py

echo.
echo NachoGPT cerrado
pause
