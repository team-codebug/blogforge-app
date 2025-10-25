#!/bin/bash

# BlogForge Setup Script
# This script sets up the virtual environment, installs dependencies, and initializes the database

set -e  # Exit on any error

echo "🚀 Starting BlogForge setup..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed. Please install pip3 first."
    exit 1
fi

echo "✅ Python 3 and pip3 are available"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed from requirements.txt"
else
    echo "⚠️ requirements.txt not found, installing common Flask dependencies..."
    pip install flask flask-sqlalchemy flask-migrate flask-login flask-wtf flask-limiter python-dotenv markdown-it-py google-genai
    echo "✅ Common dependencies installed"
fi

# Check if .flaskenv exists
if [ ! -f ".flaskenv" ]; then
    echo "📝 Creating .flaskenv file..."
    cat > .flaskenv << EOF
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///blogforge.db
GEMINI_API_KEY=your-gemini-api-key-here
EOF
    echo "✅ .flaskenv file created"
    echo "⚠️ Please update the SECRET_KEY and GEMINI_API_KEY in .flaskenv"
else
    echo "✅ .flaskenv file already exists"
fi

# Initialize database
echo "🗄️ Initializing database..."
if [ ! -d "migrations" ]; then
    echo "📊 Creating database migrations..."
    flask db init
    echo "✅ Database migrations initialized"
else
    echo "✅ Database migrations already exist"
fi

# Create initial migration if no migrations exist
if [ ! -f "migrations/versions" ] || [ -z "$(ls -A migrations/versions 2>/dev/null)" ]; then
    echo "📊 Creating initial migration..."
    flask db migrate -m "Initial migration"
    echo "✅ Initial migration created"
fi

# Apply migrations
echo "🔄 Applying database migrations..."
flask db upgrade
echo "✅ Database migrations applied"

# Create uploads directory if it doesn't exist
if [ ! -d "uploads" ]; then
    echo "📁 Creating uploads directory..."
    mkdir -p uploads
    echo "✅ Uploads directory created"
else
    echo "✅ Uploads directory already exists"
fi

echo ""
echo "🎉 BlogForge setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Update your .flaskenv file with:"
echo "   - A secure SECRET_KEY"
echo "   - Your GEMINI_API_KEY from Google AI Studio"
echo ""
echo "2. Start the application:"
echo "   source .venv/bin/activate"
echo "   flask run"
echo ""
echo "3. Open your browser and go to: http://localhost:5000"
echo ""
echo "🔧 To run the app in the future, just use:"
echo "   source .venv/bin/activate && flask run"
echo ""
