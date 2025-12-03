@echo off
REM F1 Race Replay - Backend Startup Script (Windows)

echo Starting F1 Race Replay Backend...
echo ==================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create cache directory if it doesn't exist
if not exist "cache" (
    echo Creating cache directory...
    mkdir cache
)

REM Start the backend server
echo.
echo Starting FastAPI server on http://localhost:8000
echo API documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py
