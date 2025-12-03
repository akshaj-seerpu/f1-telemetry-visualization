#!/bin/bash

# F1 Race Replay - Backend Startup Script

echo "Starting F1 Race Replay Backend..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create cache directory if it doesn't exist
if [ ! -d "cache" ]; then
    echo "Creating cache directory..."
    mkdir cache
fi

# Start the backend server
echo ""
echo "Starting FastAPI server on http://localhost:8000"
echo "API documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
