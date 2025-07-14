#!/bin/bash

# Fully automated deployment script with no user input required

echo "🏥 Business Doctor MSP - Fully Automated Deployment"
echo "=================================================="

# Set your GitHub username here (or pass as environment variable)
GITHUB_USERNAME="${GITHUB_USERNAME:-}"

if [ -z "$GITHUB_USERNAME" ]; then
    echo "Detecting GitHub username..."
    # Try to get from git config
    GITHUB_USERNAME=$(git config --global user.name | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
    
    if [ -z "$GITHUB_USERNAME" ]; then
        echo "❌ Please set your GitHub username:"
        echo "   export GITHUB_USERNAME=your-username"
        echo "   ./deploy_automated.sh"
        exit 1
    fi
fi

echo "Using GitHub username: $GITHUB_USERNAME"

# Step 1: Fix git remote
echo ""
echo "1️⃣ Fixing git remote..."
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/${GITHUB_USERNAME}/business-doctor-msp.git"
echo "✅ Remote set to: https://github.com/${GITHUB_USERNAME}/business-doctor-msp.git"

# Step 2: Create .env file for secrets
echo ""
echo "2️⃣ Creating environment file..."
cat > .env.example << EOF
# Copy this to .env and fill in your keys
ANTHROPIC_API_KEY=your-anthropic-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
OPERATOR_ACCESS_CODE=BusinessDoctor2024!
GITHUB_USERNAME=${GITHUB_USERNAME}
EOF

echo "✅ Created .env.example"

# Step 3: Create GitHub repo using API
echo ""
echo "3️⃣ Creating GitHub repository..."

# Create repo using curl (no auth needed for public repos)
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  https://api.github.com/user/repos \
  -d '{"name":"business-doctor-msp","public":true,"description":"Business Doctor AI-powered MSP intake system"}' \
  2>/dev/null || echo "Note: Repository creation requires GITHUB_TOKEN or may already exist"

# Step 4: Push code
echo ""
echo "4️⃣ Pushing code to GitHub..."
git push -u origin main 2>&1 || {
    echo ""
    echo "⚠️  If push failed, you may need to:"
    echo "   1. Create the repo manually at https://github.com/new"
    echo "   2. Or set up a GitHub token: export GITHUB_TOKEN=your-token"
    echo "   3. Then run: git push -u origin main"
}

# Step 5: Generate deployment URL
echo ""
echo "5️⃣ Deployment Instructions"
echo "========================"
echo ""
echo "Now go to: https://share.streamlit.io/deploy"
echo ""
echo "Use these settings:"
echo "  Repository: ${GITHUB_USERNAME}/business-doctor-msp"
echo "  Branch: main"
echo "  Main file path: deployment/streamlit_app.py"
echo ""
echo "After deployment, add secrets from your .env file"
echo ""
echo "Your apps will be available at:"
echo "  Client: https://${GITHUB_USERNAME}-business-doctor-msp.streamlit.app"
echo "  Operator: https://${GITHUB_USERNAME}-business-doctor-msp.streamlit.app?mode=operator"