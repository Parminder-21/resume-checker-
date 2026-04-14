@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ========================================
echo  OptiResume AI - QUICK START
echo ========================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create venv
        echo Make sure Python is installed and in PATH
        pause
        exit /b 1
    )
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install requirements
echo Installing dependencies...
pip install --quiet ^
    fastapi ^
    uvicorn ^
    python-multipart ^
    python-dotenv ^
    anthropic ^
    pydantic ^
    pydantic-settings

if errorlevel 1 (
    echo WARNING: Some packages failed to install
    echo Trying basic packages...
    pip install fastapi uvicorn python-dotenv
)

echo.
echo ========================================
echo  Starting Backend Server...
echo ========================================
echo.
echo 🚀 Server starting on http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start server
    echo Check that all dependencies are installed
    pause
)
