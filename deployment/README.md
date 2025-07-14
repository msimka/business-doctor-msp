# Business Doctor AI Intake System - Deployment Guide

## Quick Start

### Local Testing
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Add your API keys to `.streamlit/secrets.toml`:
   - Replace `your-anthropic-api-key-here` with your Anthropic API key
   - Replace `your-openai-api-key-here` with your OpenAI API key

3. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

4. Access the interfaces:
   - Client view: http://localhost:8501
   - Operator view: http://localhost:8501?mode=operator

## Deployment to Streamlit Cloud

### Step 1: Prepare GitHub Repository
1. Create a new GitHub repository
2. Upload all files from this deployment folder
3. Do NOT commit `.streamlit/secrets.toml`

### Step 2: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub account
4. Select your repository and branch
5. Set `streamlit_app.py` as the main file
6. Click "Deploy"

### Step 3: Configure Secrets
1. In Streamlit Cloud dashboard, click "Settings" → "Secrets"
2. Add your API keys:
   ```toml
   ANTHROPIC_API_KEY = "your-actual-key"
   OPENAI_API_KEY = "your-actual-key"
   SHOW_MODE_SWITCHER = false
   OPERATOR_ACCESS_CODE = "your-secure-password"
   ```

### Step 4: Share URLs
- Client intake URL: `https://your-app.streamlit.app`
- Operator console: `https://your-app.streamlit.app?mode=operator`

## Usage Instructions

### For Clients
1. Share the main URL with clients
2. They'll see the professional Glass Box interface
3. Their responses are queued for operator review

### For Operators
1. Access the operator console with `?mode=operator`
2. Use AI suggestions or compose custom responses
3. Build insights and track bottlenecks in real-time
4. Client sees polished, professional AI interface

## Security Notes

1. **Change the operator access code** in secrets
2. Consider adding authentication for operator mode
3. Never share the operator URL with clients
4. Regularly rotate API keys

## Customization

### Branding
Edit the CSS in `streamlit_app.py` to match your brand:
- Primary color: `#667eea`
- Background: `#f8f9fa`
- Update the gradient in `.client-header`

### Conversation Flow
Modify the stages in `wizard_of_oz_implementation.py`:
- Current: opening → discovery → deep_dive → synthesis
- Add industry-specific stages as needed

### AI Behavior
Adjust prompts in `_generate_ai_suggestions()` method to:
- Change conversation style
- Add industry-specific knowledge
- Modify question patterns

## Monitoring

### Track Performance
- View metrics in Streamlit Cloud dashboard
- Monitor conversation completion rates
- Track average session duration

### Iterate Based on Data
- Export conversation logs
- Analyze common bottlenecks
- Refine AI suggestions

## Scaling Beyond Pilot

After 10 successful Wizard of Oz sessions:
1. Analyze operator patterns
2. Train AI on successful conversations
3. Gradually reduce operator involvement
4. Move to full automation

## Support

For issues or questions:
- Check Streamlit Cloud logs
- Review operator console for errors
- Test locally first for debugging