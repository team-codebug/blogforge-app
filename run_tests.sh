#!/bin/bash

# BlogForge Test Runner
# This script sets up the test environment and runs the test suite

echo "🧪 BlogForge Test Runner"
echo "========================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run ./start.sh first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Install test dependencies if not already installed
echo "📥 Installing test dependencies..."
pip install -q pytest pytest-flask pytest-cov

# Set test environment variables
export FLASK_ENV=testing
export TESTING=True

# Run tests with coverage
echo "🚀 Running tests..."
echo ""

# Run specific test file
if [ "$1" = "posts" ]; then
    echo "Running posts route tests..."
    python -m pytest tests/test_posts_routes.py -v --cov=app --cov-report=term-missing
elif [ "$1" = "unit" ]; then
    echo "Running unit tests..."
    python -m pytest tests/ -k "unit" -v --cov=app --cov-report=term-missing
else
    echo "Running all tests..."
    python -m pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html:htmlcov
fi

# Check test exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    echo "📊 Coverage report generated in htmlcov/index.html"
else
    echo ""
    echo "❌ Some tests failed!"
    exit 1
fi
