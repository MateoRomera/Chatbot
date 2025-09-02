#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Inicia el EA RAG v3 Chatbot con funcionalidad de recarga de datos

.DESCRIPTION
    Este script inicia el chatbot con la nueva funcionalidad de recarga automática
    de documentos. Permite agregar nuevos archivos sin reiniciar el servidor.

.EXAMPLE
    .\start_with_reload.ps1
#>

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    EA RAG v3 Chatbot - Con Recarga" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Iniciando el chatbot con funcionalidad de recarga de datos..." -ForegroundColor Green
Write-Host ""

# 1. Cambiar al directorio del proyecto
Write-Host "1. Cambiando al directorio del proyecto..." -ForegroundColor Yellow
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# 2. Activar entorno virtual
Write-Host "2. Activando entorno virtual..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# 3. Iniciar servidor backend
Write-Host ""
Write-Host "3. Iniciando servidor backend (puerto 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptPath'; & 'venv\Scripts\Activate.ps1'; python backend\app_sqlite.py" -WindowStyle Normal

# 4. Esperar que el backend se inicie
Write-Host ""
Write-Host "4. Esperando que el backend se inicie..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# 5. Iniciar servidor frontend
Write-Host ""
Write-Host "5. Iniciando servidor frontend (puerto 8080)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptPath'; & 'venv\Scripts\Activate.ps1'; cd frontend; python -m http.server 8080" -WindowStyle Normal

# 6. Esperar que el frontend se inicie
Write-Host ""
Write-Host "6. Esperando que el frontend se inicie..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

# 7. Abrir navegador
Write-Host ""
Write-Host "7. Abriendo navegador..." -ForegroundColor Yellow
Start-Process "http://localhost:8080"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "    ¡Chatbot iniciado exitosamente!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Frontend: http://localhost:8080" -ForegroundColor Cyan
Write-Host "📍 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔄 NUEVA FUNCIONALIDAD: Recarga de Datos" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para agregar nuevos documentos:" -ForegroundColor White
Write-Host "1. Coloca tu archivo en la carpeta 'data/'" -ForegroundColor Gray
Write-Host "2. Ve a la sección 'Administración de Datos'" -ForegroundColor Gray
Write-Host "3. Haz clic en '🔄 Recargar Datos'" -ForegroundColor Gray
Write-Host "4. ¡Listo! Tu documento ya está disponible" -ForegroundColor Gray
Write-Host ""
Write-Host "Formatos soportados: .csv, .json, .xlsx, .sqlite" -ForegroundColor Magenta
Write-Host ""
Write-Host "Para probar la recarga:" -ForegroundColor White
Write-Host "- Ejecuta: python test_reload.py" -ForegroundColor Gray
Write-Host "- O ejecuta: python add_test_document.py" -ForegroundColor Gray
Write-Host ""
Write-Host "Presiona cualquier tecla para cerrar esta ventana..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
