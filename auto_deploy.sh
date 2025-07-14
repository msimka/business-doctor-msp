#!/bin/bash

# Automated deployment script for Business Doctor MSP

echo "🏥 Business Doctor MSP - Automated Deployment"
echo "============================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 required. Please install first."
    exit 1
fi

# Run the automated setup
python3 setup_github_secrets.py

# If successful, provide quick commands
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment initiated!"
    echo ""
    echo "Quick commands:"
    echo "  Watch deployment:  gh run watch"
    echo "  View logs:         gh run view --log"
    echo "  Test locally:      cd deployment && streamlit run streamlit_app.py"
    echo ""
fi