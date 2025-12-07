#!/bin/bash
# Quick start script for IconLoader

set -e  # Exit on error

echo "=========================================="
echo "IconLoader Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✓ .env created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and set your REDIS_URL before continuing!"
    echo "   Example: REDIS_URL=redis://default:your_password@your-host:6379"
    echo ""
    read -p "Press Enter after you've configured .env, or Ctrl+C to exit..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Validate setup
echo ""
echo "Validating setup..."
python validate_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Setup complete! Ready to run IconLoader"
    echo "=========================================="
    echo ""
    read -p "Run IconLoader now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python IconLoader.py
    else
        echo "To run later, use: python IconLoader.py"
    fi
else
    echo ""
    echo "❌ Setup validation failed. Please fix the issues above."
    exit 1
fi

