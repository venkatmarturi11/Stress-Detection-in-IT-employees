@echo off
echo ============================================
echo   Stress Detection System - App Startup
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
echo [1/2] Starting Python ML Backend on port %BACKEND_PORT%...
cd /d "%PROJECT_DIR%backend"
start "Django Backend" cmd /k "python manage.py runserver %BACKEND_PORT%"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend HTTP Server
echo [2/2] Starting Frontend on port %FRONTEND_PORT%...
cd /d "%PROJECT_DIR%"
start "Frontend Server" cmd /k "python -m http.server %FRONTEND_PORT%"

echo.
echo ============================================
echo   Both servers are starting!
echo ============================================
echo.
echo Frontend:     http://localhost:%FRONTEND_PORT%
echo Backend API:  http://localhost:%BACKEND_PORT%/api/health/
echo.
echo Opening application in browser...
timeout /t 2 /nobreak >nul

start http://localhost:%FRONTEND_PORT%
