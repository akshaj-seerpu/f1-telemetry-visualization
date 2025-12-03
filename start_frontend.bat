@echo off
REM F1 Race Replay - Frontend Startup Script (Windows)

echo Starting F1 Race Replay Frontend...
echo ====================================

cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Node modules not found. Installing...
    call npm install
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
)

REM Start the development server
echo.
echo Starting React development server on http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm start
