#!/usr/bin/env python3
"""
Simple deployment script that creates all necessary files for manual deployment
"""

import os
import json

def create_deployment_package():
    """Create a deployment package with instructions"""
    
    print("🏥 Business Doctor MSP - Deployment Package")
    print("=" * 50)
    
    # Create deployment instructions
    instructions = """
# Business Doctor MSP - Quick Deploy Instructions

## 1. Create GitHub Repository

Go to: https://github.com/new
- Repository name: business-doctor-msp
- Make it Public
- Don't initialize with README
- Click "Create repository"

## 2. Push Code to GitHub

Run these commands in your terminal:
```bash
cd /Users/mikesimka/STICKTOITIVITY/business-doctor-msp
git remote add origin https://github.com/YOUR_USERNAME/business-doctor-msp.git
git push -u origin main
```

## 3. Deploy to Streamlit

Go to: https://share.streamlit.io
- Click "New app"
- Repository: YOUR_USERNAME/business-doctor-msp
- Branch: main
- Main file path: deployment/streamlit_app.py
- Click "Deploy!"

## 4. Add Secrets (Important!)

After deployment starts:
1. Click the 3 dots menu → Settings → Secrets
2. Paste this configuration:

```toml
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
OPENAI_API_KEY = "your-openai-api-key-here"
SHOW_MODE_SWITCHER = false
OPERATOR_ACCESS_CODE = "BusinessDoctor2024!"
```

3. Replace with your actual API keys
4. Click Save

## 5. Your URLs

Once deployed, you'll have:
- Client Interface: https://YOUR-APP.streamlit.app
- Operator Console: https://YOUR-APP.streamlit.app?mode=operator

## 6. Test Your Deployment

1. Open client URL in one browser
2. Open operator URL in another browser
3. Type as a client
4. Respond as operator

That's it! Your Business Doctor AI is live! 🎉
"""
    
    # Write instructions
    with open("DEPLOY_NOW.md", "w") as f:
        f.write(instructions)
    
    # Create a config template
    config = {
        "github_repo": "business-doctor-msp",
        "streamlit_app": "deployment/streamlit_app.py",
        "secrets_needed": [
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY",
            "OPERATOR_ACCESS_CODE"
        ]
    }
    
    with open("deployment_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Deployment package created!")
    print("\n📄 Files created:")
    print("   - DEPLOY_NOW.md (step-by-step instructions)")
    print("   - deployment_config.json (configuration reference)")
    print("\n👉 Open DEPLOY_NOW.md and follow the instructions!")
    print("\n🚀 Estimated time to deploy: 5-10 minutes")

if __name__ == "__main__":
    create_deployment_package()