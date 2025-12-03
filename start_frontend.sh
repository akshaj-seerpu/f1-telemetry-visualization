#!/bin/bash

# F1 Race Replay - Frontend Startup Script

echo "Starting F1 Race Replay Frontend..."
echo "===================================="

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Node modules not found. Installing..."
    npm install
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Start the development server
echo ""
echo "Starting React development server on http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm start
