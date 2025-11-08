@echo off
REM EDGE-QI Frontend Quick Start Script
REM Run this script to start the development server

echo.
echo ========================================
echo   EDGE-QI Frontend Development Server
echo ========================================
echo.

cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules\" (
    echo [*] Installing dependencies...
    call npm install
    echo.
)

echo [*] Starting development server...
echo.
echo     URL: http://localhost:5173
echo.
echo     Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

call npm run dev

pause
