#!/bin/bash

# Python Space Agents Startup Script

echo "🚀 Starting Python Space Agents Setup..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Set up environment file
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "🔧 Creating .env file..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys before running the application."
fi

echo "✅ Setup completed!"
echo ""
echo "🎯 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: python main.py"
echo "3. Or run the example: python example.py"
echo ""
echo "🧪 Run tests with: python -m pytest tests/"
echo ""
echo "📚 To activate the virtual environment manually:"
echo "   source venv/bin/activate"
