@echo off
REM Desktop AI Companion - Windows Startup Script

echo Starting Desktop AI Companion...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if dependencies are installed
echo Checking dependencies...
pip install -q -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo.
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and add your ANTHROPIC_API_KEY
    echo.
    pause
    exit /b 1
)

REM Run the application
echo.
echo Launching AI Companion...
echo.
python desktop_companion.py

pause
