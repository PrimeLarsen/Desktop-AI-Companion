#!/bin/bash
# Desktop AI Companion - Mac/Linux Startup Script

echo "Starting Desktop AI Companion..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
echo "Checking dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and add your ANTHROPIC_API_KEY"
    echo ""
    exit 1
fi

# Run the application
echo ""
echo "Launching AI Companion..."
echo ""
python desktop_companion.py
