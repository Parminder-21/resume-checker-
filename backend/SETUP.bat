@echo off
cd /d "%~dp0"
echo.
echo ========================================
echo  OptiResume AI - Backend Setup
echo ========================================
echo.

REM Create fresh virtual environment
echo Cleaning old venv...
if exist venv rmdir /s /q venv
echo Creating fresh venv...
python -m venv venv

echo.
echo Activating venv...
call venv\Scripts\activate.bat

echo.
echo Installing pip and tools...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Installing requirements...
pip install -r requirements.txt

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo To start the server, run:
echo   venv\Scripts\python run.py
echo.
pause
