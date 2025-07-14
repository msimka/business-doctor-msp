# Business Doctor AI - Deployment Guide

## Quick Start

1. **Set up Google API Key**:
   ```bash
   cd deployment
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # Edit .streamlit/secrets.toml and add your Google API key
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally**:
   ```bash
   # Option 1: Use the run script
   ./run_app.sh
   
   # Option 2: Direct streamlit command
   streamlit run streamlit_app.py
   ```

4. **Access the app**:
   - Client view: http://localhost:8501
   - Operator view: http://localhost:8501/?mode=operator

## Streamlit Cloud Deployment

1. **Push to GitHub** (ensure secrets.toml is in .gitignore)

2. **Deploy on Streamlit Cloud**:
   - Go to https://share.streamlit.io/
   - Connect your GitHub repository
   - Select branch and file: `deployment/streamlit_app.py`
   
3. **Configure Secrets**:
   - In Streamlit Cloud settings, add:
     ```
     GOOGLE_API_KEY = "your-api-key"
     SHOW_MODE_SWITCHER = false
     ```

## Troubleshooting

### Import Errors
- Ensure you're running from the `deployment` directory
- The app automatically adds parent directories to Python path

### Google API Errors
- Verify your API key is correct
- Check that the Gemini API is enabled in your Google Cloud project
- Ensure you have sufficient quota

### Page Config Errors
- The page config is set only once in the main app
- Don't call `st.set_page_config()` in imported modules

### Async Errors
- The app uses nest-asyncio to handle async operations
- Ensure nest-asyncio is installed: `pip install nest-asyncio`