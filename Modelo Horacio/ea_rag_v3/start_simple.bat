@echo off
echo ========================================
echo    EA RAG v3 Chatbot - Inicio Simple
echo ========================================
echo.

REM Obtener el directorio donde está este script
set SCRIPT_DIR=%~dp0
echo Directorio del proyecto: %SCRIPT_DIR%

REM Cambiar al directorio del proyecto
cd /d "%SCRIPT_DIR%"

echo.
echo 1. Verificando que estamos en el directorio correcto...
if not exist "backend\app_sqlite.py" (
    echo ERROR: No se encontró backend\app_sqlite.py
    echo Asegúrate de ejecutar este script desde el directorio raíz del proyecto
    pause
    exit /b 1
)

echo 2. Verificando entorno virtual...
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: No se encontró el entorno virtual
    echo Ejecuta: python -m venv venv
    pause
    exit /b 1
)

echo 3. Activando entorno virtual...
call venv\Scripts\activate.bat

echo 4. Verificando dependencias...
python -c "import fastapi, uvicorn, pandas" 2>nul
if errorlevel 1 (
    echo Instalando dependencias...
    pip install fastapi uvicorn pandas openpyxl python-dotenv
)

echo.
echo 5. Iniciando servidor backend (puerto 8000)...
start "Backend" cmd /k "cd /d "%SCRIPT_DIR%" && venv\Scripts\activate.bat && python backend\app_sqlite.py"

echo 6. Esperando que el backend se inicie...
timeout /t 5 /nobreak > nul

echo 7. Iniciando servidor frontend (puerto 8080)...
start "Frontend" cmd /k "cd /d "%SCRIPT_DIR%" && venv\Scripts\activate.bat && cd frontend && python -m http.server 8080"

echo 8. Esperando que el frontend se inicie...
timeout /t 3 /nobreak > nul

echo 9. Abriendo navegador...
start http://localhost:8080

echo.
echo ========================================
echo    ¡Chatbot iniciado exitosamente!
echo ========================================
echo.
echo 📍 Frontend: http://localhost:8080
echo 📍 Backend API: http://localhost:8000
echo.
echo 🔄 Para recargar datos:
echo    1. Ve a la sección "Administración de Datos"
echo    2. Haz clic en "🔄 Recargar Datos"
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause > nul
