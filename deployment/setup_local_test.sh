#!/bin/bash

# Business Doctor AI - Local Testing Setup Script

echo "🏥 Business Doctor AI - Local Setup"
echo "=================================="

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # macOS/Linux
    source venv/bin/activate
fi

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p .streamlit
mkdir -p ../intake-system

# Copy parent directory files for imports
echo "📋 Setting up imports..."
cp -r ../intake-system/* ../intake-system/ 2>/dev/null || echo "⚠️ Note: Some intake-system files not found"

# Check for secrets file
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "⚠️ Warning: .streamlit/secrets.toml not found!"
    echo "Please add your API keys to .streamlit/secrets.toml before running"
fi

# Create run script
cat > run_local.sh << 'EOF'
#!/bin/bash
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
streamlit run streamlit_app.py
EOF

chmod +x run_local.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add your API keys to .streamlit/secrets.toml"
echo "2. Run the app with: ./run_local.sh"
echo "3. Open http://localhost:8501 for client view"
echo "4. Open http://localhost:8501?mode=operator for operator view"
echo ""
echo "🚀 Happy testing!"