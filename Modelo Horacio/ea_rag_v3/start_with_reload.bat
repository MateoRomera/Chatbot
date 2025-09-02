@echo off
echo ========================================
echo    EA RAG v3 Chatbot - Con Recarga
echo ========================================
echo.

echo Iniciando el chatbot con funcionalidad de recarga de datos...
echo.

echo 1. Cambiando al directorio del proyecto...
cd /d "%~dp0"

echo 2. Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo 3. Iniciando servidor backend (puerto 8000)...
start "Backend" cmd /k "cd /d "%~dp0" && venv\Scripts\activate.bat && python backend\app_sqlite.py"

echo.
echo 4. Esperando que el backend se inicie...
timeout /t 3 /nobreak > nul

echo.
echo 5. Iniciando servidor frontend (puerto 8080)...
start "Frontend" cmd /k "cd /d "%~dp0" && venv\Scripts\activate.bat && cd frontend && python -m http.server 8080"

echo.
echo 6. Esperando que el frontend se inicie...
timeout /t 2 /nobreak > nul

echo.
echo 7. Abriendo navegador...
start http://localhost:8080

echo.
echo ========================================
echo    ¡Chatbot iniciado exitosamente!
echo ========================================
echo.
echo 📍 Frontend: http://localhost:8080
echo 📍 Backend API: http://localhost:8000
echo.
echo 🔄 NUEVA FUNCIONALIDAD: Recarga de Datos
echo.
echo Para agregar nuevos documentos:
echo 1. Coloca tu archivo en la carpeta 'data/'
echo 2. Ve a la sección "Administración de Datos"
echo 3. Haz clic en "🔄 Recargar Datos"
echo 4. ¡Listo! Tu documento ya está disponible
echo.
echo Formatos soportados: .csv, .json, .xlsx, .sqlite
echo.
echo Para probar la recarga:
echo - Ejecuta: python test_reload.py
echo - O ejecuta: python add_test_document.py
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause > nul
