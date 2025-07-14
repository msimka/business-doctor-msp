#!/usr/bin/env python3
"""
Streamlit deployment helper - opens the deployment page with pre-filled values
"""

import webbrowser
import urllib.parse
import time

def deploy_to_streamlit():
    """Open Streamlit deployment page with pre-filled repository info"""
    
    print("🚀 Launching Streamlit Cloud Deployment")
    print("=" * 50)
    
    # Construct deployment URL with parameters
    base_url = "https://share.streamlit.io/deploy"
    params = {
        "repository": "msimka/business-doctor-msp",
        "branch": "main",
        "mainModule": "deployment/streamlit_app.py"
    }
    
    # Create full URL
    query_string = urllib.parse.urlencode(params)
    deploy_url = f"{base_url}?{query_string}"
    
    print("\n📋 Deployment Settings:")
    print(f"   Repository: msimka/business-doctor-msp")
    print(f"   Branch: main")
    print(f"   Main file: deployment/streamlit_app.py")
    
    print("\n🌐 Opening Streamlit Cloud in your browser...")
    print("   If browser doesn't open, go to:")
    print(f"   {deploy_url}")
    
    # Open browser
    webbrowser.open(deploy_url)
    
    print("\n📝 After deployment page opens:")
    print("   1. Click 'Deploy!' button")
    print("   2. Wait for app to build (~2-5 minutes)")
    print("   3. Click Settings → Secrets")
    print("   4. Add your API keys")
    
    print("\n🔑 Secrets to add:")
    print("""
ANTHROPIC_API_KEY = "your-anthropic-api-key"
OPENAI_API_KEY = "your-openai-api-key"
OPERATOR_ACCESS_CODE = "BusinessDoctor2024!"
SHOW_MODE_SWITCHER = false
    """)
    
    print("\n🎯 Your app URLs will be:")
    print("   Client: https://msimka-business-doctor-msp.streamlit.app")
    print("   Operator: https://msimka-business-doctor-msp.streamlit.app?mode=operator")
    
    print("\n✅ Deployment helper complete!")

if __name__ == "__main__":
    deploy_to_streamlit()