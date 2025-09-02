@echo off
echo Starting EA RAG v3 Chatbot...
echo.

echo Starting Backend Server (SQLite)...
start "Backend Server" cmd /k "venv\Scripts\activate && python backend\app_sqlite.py"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && python -m http.server 8080"

echo.
echo Chatbot is starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8080
echo.
echo Press any key to open the frontend in your browser...
pause > nul

start http://localhost:8080

echo.
echo Servers are running. Press Ctrl+C in each window to stop them.
pause
