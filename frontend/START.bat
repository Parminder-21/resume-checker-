@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ========================================
echo  OptiResume AI - Frontend Setup
echo ========================================
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing npm dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: npm install failed
        echo Make sure Node.js and npm are installed
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo  Starting Frontend Dev Server...
echo ========================================
echo.
echo 🌐 Frontend starting on http://localhost:5173
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start dev server
    pause
)
