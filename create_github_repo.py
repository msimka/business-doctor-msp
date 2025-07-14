#!/usr/bin/env python3
"""
Create GitHub repo programmatically without requiring GitHub CLI
"""

import subprocess
import os
import sys
import urllib.request
import urllib.error
import json

def get_github_username():
    """Get GitHub username from git config or environment"""
    # Try environment variable first
    username = os.environ.get('GITHUB_USERNAME')
    if username:
        return username
    
    # Try git config
    try:
        result = subprocess.run(['git', 'config', '--global', 'user.email'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            # Extract username from email if it's a github email
            email = result.stdout.strip()
            if '@' in email:
                return email.split('@')[0]
    except:
        pass
    
    return None

def setup_git_remote(username):
    """Fix git remote with correct username"""
    print(f"Setting up git remote for user: {username}")
    
    # Remove existing origin
    subprocess.run(['git', 'remote', 'remove', 'origin'], 
                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    
    # Add correct origin
    remote_url = f"https://github.com/{username}/business-doctor-msp.git"
    subprocess.run(['git', 'remote', 'add', 'origin', remote_url])
    
    print(f"✅ Remote set to: {remote_url}")
    return remote_url

def create_github_repo_instructions(username):
    """Generate instructions for manual repo creation"""
    print("\n📋 Manual Repository Creation Instructions")
    print("=" * 50)
    print("\n1. Open your browser and go to:")
    print("   https://github.com/new")
    print("\n2. Create repository with these settings:")
    print(f"   - Repository name: business-doctor-msp")
    print("   - Description: Business Doctor AI-powered MSP intake system")
    print("   - Public repository: ✓")
    print("   - Initialize with README: ✗ (leave unchecked)")
    print("\n3. Click 'Create repository'")
    print("\n4. Come back here and run:")
    print(f"   git push -u origin main")
    
def main():
    print("🏥 Business Doctor MSP - GitHub Repository Setup")
    print("=" * 50)
    
    # Get username
    username = get_github_username()
    
    if not username:
        print("\n❌ GitHub username not found!")
        print("\nPlease run one of these commands first:")
        print("  export GITHUB_USERNAME=your-github-username")
        print("  git config --global user.email your-email@example.com")
        sys.exit(1)
    
    # Setup remote
    remote_url = setup_git_remote(username)
    
    # Try to push
    print("\n🚀 Attempting to push to GitHub...")
    result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Successfully pushed to GitHub!")
        print(f"\n🎉 Your repository is live at:")
        print(f"   https://github.com/{username}/business-doctor-msp")
    else:
        if "Repository not found" in result.stderr:
            print("\n⚠️  Repository doesn't exist yet.")
            create_github_repo_instructions(username)
        else:
            print(f"\n❌ Push failed: {result.stderr}")
    
    # Streamlit deployment instructions
    print("\n\n📱 Streamlit Deployment")
    print("=" * 50)
    print("\n1. Go to: https://share.streamlit.io")
    print("2. Click 'New app'")
    print("3. Enter these settings:")
    print(f"   - Repository: {username}/business-doctor-msp")
    print("   - Branch: main")
    print("   - Main file path: deployment/streamlit_app.py")
    print("\n4. Click 'Deploy!'")
    print("\n5. Add your API keys in Settings → Secrets")
    print("\n📱 Your apps will be available at:")
    print(f"   Client: https://{username}-business-doctor-msp.streamlit.app")
    print(f"   Operator: https://{username}-business-doctor-msp.streamlit.app?mode=operator")

if __name__ == "__main__":
    main()