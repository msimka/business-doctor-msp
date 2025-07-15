#!/bin/bash

# Business Doctor Terminal Application Launcher

echo "🏥 Business Doctor AI - Terminal Version"
echo "======================================"

# Check if API key is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo ""
    echo "⚠️  Google API key not found!"
    echo ""
    echo "Please set your API key:"
    echo "  export GOOGLE_API_KEY='your-gemini-api-key'"
    echo ""
    echo "Using your backup key:"
    echo "  export GOOGLE_API_KEY='AIzaSyC0r-ujNDB0Wrpz4_MDUwP1a0yV7zPWqek'"
    echo ""
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Install dependencies if needed
if ! python3 -c "import google.generativeai" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install google-generativeai
fi

# Run the application
echo ""
echo "Starting Business Doctor AI..."
echo ""

python3 core/terminal_app.py