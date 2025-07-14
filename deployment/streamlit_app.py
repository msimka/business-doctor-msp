"""
Business Doctor AI Intake System - Main Application
Deployment version with both client and operator interfaces
"""

import streamlit as st
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'intake-system'))

from wizard_of_oz_implementation import WizardOfOzInterface

# Configure page based on mode
query_params = st.query_params
mode = query_params.get("mode", "client")

if mode == "operator":
    st.set_page_config(
        page_title="Operator Console - Business Doctor",
        page_icon="🎛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
else:
    st.set_page_config(
        page_title="Business Doctor AI Consultation",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

# Add custom CSS for professional styling
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Professional color scheme */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Client view styling */
    .client-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    /* Glass box effect */
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMarkdown"]) {
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Operator console styling */
    .operator-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: white;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Metrics styling */
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 20px;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize and render the appropriate interface
def main():
    # Create interface instance
    woz = WizardOfOzInterface()
    
    # Add mode switcher for development
    if st.secrets.get("SHOW_MODE_SWITCHER", False):
        with st.sidebar:
            st.divider()
            st.caption("Development Tools")
            if mode == "client":
                if st.button("🎛️ Switch to Operator View"):
                    st.query_params["mode"] = "operator"
                    st.rerun()
            else:
                if st.button("👤 Switch to Client View"):
                    st.query_params["mode"] = "client"
                    st.rerun()
    
    # Add operator instructions
    if mode == "operator":
        st.markdown("""
        <div class="operator-warning">
        <strong>⚠️ Operator Mode</strong><br>
        This is the hidden operator interface. Clients access the system without the ?mode=operator parameter.
        </div>
        """, unsafe_allow_html=True)
    
    # Render the interface
    woz.render()
    
    # Add footer for client view
    if mode == "client":
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                "<center><small>Powered by Business Doctor AI | Your business transformation partner</small></center>",
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()