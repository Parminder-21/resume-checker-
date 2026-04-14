@echo off
echo.
echo ========================================
echo  OptiResume AI - Full Stack Launcher
echo ========================================
echo.
echo This will start both frontend and backend
echo in separate windows.
echo.
echo Choose an option:
echo.
echo 1) Start Backend Only
echo 2) Start Frontend Only
echo 3) Start Both (Recommended)
echo 4) Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Starting Backend...
    start "OptiResume Backend" cmd /k "cd backend && call START.bat"
) else if "%choice%"=="2" (
    echo.
    echo First, make sure the BACKEND is already running!
    echo.
    echo Starting Frontend...
    start "OptiResume Frontend" cmd /k "cd frontend && call START.bat"
) else if "%choice%"=="3" (
    echo Starting Backend...
    start "OptiResume Backend" cmd /k "cd backend && call START.bat"
    
    timeout /t 3 /nobreak
    
    echo Starting Frontend...
    start "OptiResume Frontend" cmd /k "cd frontend && call START.bat"
    
    echo.
    echo ========================================
    echo Both servers should now be running!
    echo ========================================
    echo.
    echo 🚀 Backend: http://localhost:8000
    echo 🌐 Frontend: http://localhost:5173
    echo.
    echo API Docs: http://localhost:8000/docs
    echo.
) else (
    echo Exiting...
    exit /b 0
)
