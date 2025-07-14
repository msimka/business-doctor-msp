#!/usr/bin/env python3
"""
Programmatically set up GitHub secrets for automated deployment
"""

import subprocess
import sys
import json
import getpass

def run_command(cmd):
    """Run shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return result.stdout.strip()

def setup_github_cli():
    """Ensure GitHub CLI is installed and authenticated"""
    # Check if gh is installed
    gh_version = run_command("gh --version")
    if not gh_version:
        print("Installing GitHub CLI...")
        if sys.platform == "darwin":
            # macOS
            run_command("curl -L https://github.com/cli/cli/releases/download/v2.40.0/gh_2.40.0_macOS_arm64.tar.gz | tar xz")
            run_command("sudo mv gh_2.40.0_macOS_arm64/bin/gh /usr/local/bin/")
        else:
            print("Please install GitHub CLI manually: https://cli.github.com")
            sys.exit(1)
    
    # Check authentication
    auth_status = run_command("gh auth status")
    if "Logged in" not in str(auth_status):
        print("Authenticating with GitHub...")
        run_command("gh auth login --web")

def create_github_repo():
    """Create GitHub repository"""
    print("Creating GitHub repository...")
    result = run_command("gh repo create business-doctor-msp --public --source=. --remote=origin --push")
    if result:
        print("✅ Repository created and pushed!")
    else:
        # Repo might already exist
        print("Repository may already exist. Pushing changes...")
        run_command("git remote add origin https://github.com/$(gh api user -q .login)/business-doctor-msp.git 2>/dev/null || true")
        run_command("git push -u origin main")

def set_github_secrets():
    """Set up GitHub secrets for deployment"""
    print("\n📝 Setting up GitHub Secrets...")
    print("=" * 50)
    
    secrets = {
        "ANTHROPIC_API_KEY": getpass.getpass("Enter your Anthropic API key: "),
        "OPENAI_API_KEY": getpass.getpass("Enter your OpenAI API key: "),
        "OPERATOR_ACCESS_CODE": getpass.getpass("Enter operator access code (default: BusinessDoctor2024!): ") or "BusinessDoctor2024!",
        "STREAMLIT_API_TOKEN": getpass.getpass("Enter Streamlit API token (optional, press Enter to skip): ")
    }
    
    # Set secrets using GitHub CLI
    for key, value in secrets.items():
        if value:  # Only set non-empty secrets
            cmd = f'gh secret set {key} --body "{value}"'
            result = run_command(cmd)
            if result is not None:
                print(f"✅ Set secret: {key}")
            else:
                print(f"❌ Failed to set secret: {key}")

def trigger_deployment():
    """Trigger GitHub Actions deployment"""
    print("\n🚀 Triggering deployment...")
    
    # Enable GitHub Actions if needed
    run_command("gh api repos/{owner}/{repo}/actions/permissions -X PUT -f enabled=true")
    
    # Trigger workflow
    result = run_command("gh workflow run deploy.yml")
    if result is not None:
        print("✅ Deployment triggered!")
        print("\nView deployment progress:")
        print("gh run watch")
        print("\nOr visit: https://github.com/$(gh api user -q .login)/business-doctor-msp/actions")

def get_streamlit_instructions():
    """Provide Streamlit setup instructions"""
    username = run_command("gh api user -q .login")
    
    print("\n📱 Streamlit Cloud Setup")
    print("=" * 50)
    print("\nSince Streamlit doesn't have a full API yet, complete setup at:")
    print("https://share.streamlit.io/deploy")
    print("\nUse these settings:")
    print(f"  Repository: {username}/business-doctor-msp")
    print("  Branch: main")
    print("  Main file: deployment/streamlit_app.py")
    print("\nYour app will be available at:")
    print(f"  Client: https://YOUR-APP-NAME.streamlit.app")
    print(f"  Operator: https://YOUR-APP-NAME.streamlit.app?mode=operator")

def main():
    """Main setup flow"""
    print("🏥 Business Doctor MSP - Automated Deployment Setup")
    print("=" * 50)
    
    # Step 1: Setup GitHub CLI
    print("\n1️⃣ Setting up GitHub CLI...")
    setup_github_cli()
    
    # Step 2: Create repository
    print("\n2️⃣ Creating GitHub repository...")
    create_github_repo()
    
    # Step 3: Set secrets
    print("\n3️⃣ Configuring secrets...")
    set_github_secrets()
    
    # Step 4: Trigger deployment
    print("\n4️⃣ Starting deployment...")
    trigger_deployment()
    
    # Step 5: Final instructions
    print("\n5️⃣ Final steps...")
    get_streamlit_instructions()
    
    print("\n✅ Setup complete! Your Business Doctor AI system is deploying.")

if __name__ == "__main__":
    main()