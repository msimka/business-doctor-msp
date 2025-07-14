#!/bin/bash

echo "🚀 Business Doctor MSP - Streamlit Deployment Script"
echo "===================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: GitHub Setup
echo -e "${YELLOW}Step 1: GitHub Repository Setup${NC}"
echo "--------------------------------"
echo ""
echo "First, we need to push your code to GitHub."
echo ""
echo "Option A: Using GitHub CLI (recommended):"
echo "  1. Install GitHub CLI: https://cli.github.com"
echo "  2. Run: gh auth login"
echo "  3. Run: gh repo create business-doctor-msp --public --source=. --remote=origin --push"
echo ""
echo "Option B: Manual setup:"
echo "  1. Go to https://github.com/new"
echo "  2. Name: business-doctor-msp"
echo "  3. Make it public"
echo "  4. Don't initialize with README"
echo "  5. Run these commands:"
echo ""
echo "     git remote add origin https://github.com/YOUR_USERNAME/business-doctor-msp.git"
echo "     git push -u origin main"
echo ""
read -p "Press Enter when GitHub repo is created and pushed..."

# Step 2: Streamlit Cloud Setup
echo ""
echo -e "${YELLOW}Step 2: Streamlit Cloud Deployment${NC}"
echo "-----------------------------------"
echo ""
echo "1. Go to: https://share.streamlit.io"
echo "2. Click 'New app'"
echo "3. Fill in:"
echo "   - Repository: YOUR_USERNAME/business-doctor-msp"
echo "   - Branch: main"
echo "   - Main file path: deployment/streamlit_app.py"
echo "4. Click 'Deploy'"
echo ""
read -p "Press Enter when deployment is started..."

# Step 3: Configure Secrets
echo ""
echo -e "${YELLOW}Step 3: Configure Secrets${NC}"
echo "-------------------------"
echo ""
echo "While app is deploying:"
echo "1. Click on 'Manage app' (3 dots menu)"
echo "2. Go to 'Settings' → 'Secrets'"
echo "3. Paste this configuration:"
echo ""
cat << 'EOF'
ANTHROPIC_API_KEY = "your-anthropic-api-key"
OPENAI_API_KEY = "your-openai-api-key"
SHOW_MODE_SWITCHER = false
OPERATOR_ACCESS_CODE = "BusinessDoctor2024!"
EOF
echo ""
echo "4. Replace with your actual API keys"
echo "5. Click 'Save'"
echo ""
read -p "Press Enter when secrets are configured..."

# Step 4: Get URLs
echo ""
echo -e "${YELLOW}Step 4: Your App URLs${NC}"
echo "---------------------"
echo ""
echo "Your app should now be live at:"
echo ""
echo -e "${GREEN}Client Interface:${NC}"
echo "https://YOUR-APP-NAME.streamlit.app"
echo ""
echo -e "${GREEN}Operator Console:${NC}"
echo "https://YOUR-APP-NAME.streamlit.app?mode=operator"
echo ""
echo "The exact URL will be shown in Streamlit Cloud dashboard."
echo ""

# Step 5: Test Instructions
echo -e "${YELLOW}Step 5: Testing Your Deployment${NC}"
echo "-------------------------------"
echo ""
echo "1. Open the client URL in one browser/tab"
echo "2. Open the operator URL in another browser/tab"
echo "3. Type in the client interface"
echo "4. Use operator console to respond"
echo ""

# Step 6: Quick Commands
echo -e "${YELLOW}Useful Commands:${NC}"
echo "----------------"
echo ""
echo "View logs:"
echo "  - Check Streamlit Cloud dashboard → Manage app → Logs"
echo ""
echo "Update app:"
echo "  - git add ."
echo "  - git commit -m 'Update message'"
echo "  - git push"
echo "  - App auto-updates in ~30 seconds"
echo ""
echo "Local testing:"
echo "  - cd deployment"
echo "  - streamlit run streamlit_app.py"
echo ""

echo -e "${GREEN}✅ Deployment guide complete!${NC}"
echo ""
echo "Need help? Check deployment/README.md for detailed instructions."