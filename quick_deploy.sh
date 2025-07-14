#!/bin/bash

echo "🏥 Quick Deploy Commands for Business Doctor MSP"
echo "=============================================="
echo ""
echo "Your GitHub username: MychalSimka"
echo ""
echo "1️⃣ First, create repo at: https://github.com/new"
echo "   Name: business-doctor-msp"
echo ""
echo "2️⃣ Then run this command:"
echo "   git push -u origin main"
echo ""
echo "3️⃣ Deploy at: https://share.streamlit.io"
echo "   Repo: MychalSimka/business-doctor-msp"
echo "   File: deployment/streamlit_app.py"
echo ""
echo "Ready? Let's push your code now..."
echo ""
read -p "Press Enter after creating GitHub repo..."

git push -u origin main

echo ""
echo "✅ Code pushed! Now go deploy on Streamlit Cloud."