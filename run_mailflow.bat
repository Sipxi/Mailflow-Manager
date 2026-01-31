@echo off
REM Mail Flow Manager Launcher Script
REM This script launches the Mail Flow Manager application

echo ====================================================
echo            Mail Flow Manager Launcher
echo ====================================================
echo.

REM Change to the script's directory
cd /d "%~dp0"

REM Check if Python is installed and accessible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and add it to your PATH environment variable
    echo.
    pause
    exit /b 1
)

REM Display current directory and Python version
echo Current directory: %CD%
python --version
echo.

REM Check if main.py exists
if not exist "main.py" (
    echo ERROR: main.py not found in current directory
    echo Please make sure you're running this script from the correct folder
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed (optional check)
echo Checking dependencies...
python -c "import requests, dotenv" >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Some dependencies may be missing
    echo You may need to run: pip install -r requirements.txt
    echo.
)

REM Launch the Mail Flow Manager
echo Starting Mail Flow Manager...
echo.
echo Press Ctrl+C to stop the application
echo ====================================================
echo.

python main.py

REM Handle exit codes
if %errorlevel% neq 0 (
    echo.
    echo ====================================================
    echo Application exited with error code: %errorlevel%
    echo ====================================================
) else (
    echo.
    echo ====================================================
    echo Mail Flow Manager finished successfully
    echo ====================================================
)

echo.
pause