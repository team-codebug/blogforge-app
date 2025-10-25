#!/bin/bash

# BlogForge Run Script
# Simple script to start the Flask application

echo "🚀 Starting BlogForge..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run ./start.sh first to set up the project."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if .flaskenv exists
if [ ! -f ".flaskenv" ]; then
    echo "❌ .flaskenv file not found. Please run ./start.sh first to set up the project."
    exit 1
fi

# Start the Flask application
echo "🌐 Starting Flask application..."
echo "📍 Application will be available at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

flask run --no-debugger --reload -p 5000
