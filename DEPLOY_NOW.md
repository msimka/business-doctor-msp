
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
