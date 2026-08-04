@echo off
echo ============================================
echo   Stress Detection System - Server Startup
echo ============================================
echo.

REM Configuration
set PROJECT_DIR=%~dp0
set FRONTEND_PORT=3000
set BACKEND_PORT=8000

echo Project Directory: %PROJECT_DIR%
echo.
echo Frontend: http://localhost:%FRONTEND_PORT%
echo Backend API: http://localhost:%BACKEND_PORT%/api/
echo.

REM Start Python Django Backend
echo [1/1] Starting Stress Detection System on port %BACKEND_PORT%...
cd /d "%PROJECT_DIR%backend"
start "Stress Detection Backend" cmd /k "python manage.py runserver %BACKEND_PORT%"

echo.
echo ============================================
echo   System is starting!
echo ============================================
echo.
echo Home Page:      http://localhost:%BACKEND_PORT%
echo Backend API:    http://localhost:%BACKEND_PORT%/api/health/
echo.
echo Opening application in browser...
ping 127.0.0.1 -n 5 > nul

start "" "http://localhost:%BACKEND_PORT%"
