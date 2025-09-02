# Start EA RAG v3 Chatbot
Write-Host "Starting EA RAG v3 Chatbot..." -ForegroundColor Green
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Start backend server
Write-Host "Starting Backend Server (SQLite)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "venv\Scripts\Activate.ps1; python backend\app_sqlite.py" -WindowStyle Normal

# Wait for backend to start
Write-Host "Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Start frontend server
Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; python -m http.server 8080" -WindowStyle Normal

Write-Host ""
Write-Host "Chatbot is starting..." -ForegroundColor Green
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""

# Open browser
Write-Host "Opening frontend in browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8080"

Write-Host "Servers are running. Close the PowerShell windows to stop them." -ForegroundColor Green
Write-Host "Press any key to exit this script..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
