@echo off
REM Puff n' Fleur Setup Script for Windows

echo.
echo ========================================
echo  Puff n' Fleur - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   1. Open this folder in a terminal
echo   2. Run: venv\Scripts\activate
echo   3. Run: python app.py
echo   4. Open: http://localhost:5000
echo.
echo Happy planning! 🎈
echo.
pause
