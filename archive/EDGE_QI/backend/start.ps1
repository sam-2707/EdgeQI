# EDGE-QI Backend Quick Start Script
# This script sets up and runs the backend server

Write-Host "🚀 EDGE-QI Backend Quick Start" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "❌ Python not found. Please install Python 3.9+." -ForegroundColor Red
    exit 1
}

$pythonVersion = python --version
Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Navigate to backend directory
$backendDir = "d:\EDGE_QI_!\EDGE_QI\backend"
Set-Location $backendDir

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q --upgrade pip
pip install -q -r requirements.txt
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Check PostgreSQL
Write-Host "Database Configuration:" -ForegroundColor Yellow
Write-Host "  - Make sure PostgreSQL is running" -ForegroundColor White
Write-Host "  - Create database: CREATE DATABASE edge_qi;" -ForegroundColor White
Write-Host "  - Default connection: postgresql://postgres:postgres@localhost:5432/edge_qi" -ForegroundColor White
Write-Host ""

# Start server
Write-Host "Starting FastAPI server..." -ForegroundColor Yellow
Write-Host "  - API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  - WebSocket: ws://localhost:8000/socket.io" -ForegroundColor Cyan
Write-Host "  - Press Ctrl+C to stop" -ForegroundColor White
Write-Host ""

# Run server
python -m uvicorn src.main:socket_app --reload --port 8000 --host 0.0.0.0
