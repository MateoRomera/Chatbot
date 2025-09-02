#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Inicia el EA RAG v3 Chatbot de forma simple y robusta

.DESCRIPTION
    Este script inicia el chatbot verificando que todo esté en su lugar
    y manejando errores comunes.

.EXAMPLE
    .\start_simple.ps1
#>

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    EA RAG v3 Chatbot - Inicio Simple" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Obtener el directorio donde está este script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Directorio del proyecto: $scriptPath" -ForegroundColor Gray

# Cambiar al directorio del proyecto
Set-Location $scriptPath

Write-Host ""
Write-Host "1. Verificando que estamos en el directorio correcto..." -ForegroundColor Yellow
if (-not (Test-Path "backend\app_sqlite.py")) {
    Write-Host "ERROR: No se encontró backend\app_sqlite.py" -ForegroundColor Red
    Write-Host "Asegúrate de ejecutar este script desde el directorio raíz del proyecto" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "2. Verificando entorno virtual..." -ForegroundColor Yellow
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "ERROR: No se encontró el entorno virtual" -ForegroundColor Red
    Write-Host "Ejecuta: python -m venv venv" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "3. Activando entorno virtual..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

Write-Host "4. Verificando dependencias..." -ForegroundColor Yellow
try {
    python -c "import fastapi, uvicorn, pandas" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Dependencias faltantes"
    }
} catch {
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install fastapi uvicorn pandas openpyxl python-dotenv
}

Write-Host ""
Write-Host "5. Iniciando servidor backend (puerto 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptPath'; & 'venv\Scripts\Activate.ps1'; python backend\app_sqlite.py" -WindowStyle Normal

Write-Host "6. Esperando que el backend se inicie..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "7. Iniciando servidor frontend (puerto 8080)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptPath'; & 'venv\Scripts\Activate.ps1'; cd frontend; python -m http.server 8080" -WindowStyle Normal

Write-Host "8. Esperando que el frontend se inicie..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "9. Abriendo navegador..." -ForegroundColor Yellow
Start-Process "http://localhost:8080"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "    ¡Chatbot iniciado exitosamente!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Frontend: http://localhost:8080" -ForegroundColor Cyan
Write-Host "📍 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔄 Para recargar datos:" -ForegroundColor Yellow
Write-Host "   1. Ve a la sección 'Administración de Datos'" -ForegroundColor Gray
Write-Host "   2. Haz clic en '🔄 Recargar Datos'" -ForegroundColor Gray
Write-Host ""
Write-Host "Presiona cualquier tecla para cerrar esta ventana..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
