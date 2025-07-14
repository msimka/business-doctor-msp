#!/bin/bash

# Business Doctor Streamlit App Runner

# Set the working directory to the deployment folder
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if secrets.toml exists
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "WARNING: .streamlit/secrets.toml not found!"
    echo "Please copy .streamlit/secrets.toml.example to .streamlit/secrets.toml"
    echo "and add your Google API key."
    exit 1
fi

# Run the Streamlit app
echo "Starting Business Doctor AI..."
streamlit run streamlit_app.py