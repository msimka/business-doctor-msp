"""
Simple test version of the Business Doctor app
"""

import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(
    page_title="Business Doctor AI - Test",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Business Doctor AI - Test Version")

# Test basic functionality
col1, col2 = st.columns(2)

with col1:
    st.header("💬 Chat Test")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Tell me about your business..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Test Gemini API
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(f"As a business consultant, respond to: {prompt}")
                    
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with col2:
    st.header("🧠 System Status")
    
    # Check secrets
    st.subheader("Configuration Check")
    
    has_api_key = "GOOGLE_API_KEY" in st.secrets
    st.write(f"✅ Google API Key: {'Found' if has_api_key else 'Missing'}")
    
    has_operator_code = "OPERATOR_ACCESS_CODE" in st.secrets
    st.write(f"✅ Operator Code: {'Found' if has_operator_code else 'Missing'}")
    
    # Test API
    if st.button("Test Gemini API"):
        try:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-pro')
            result = model.generate_content("Say 'API is working!' in 5 words or less")
            st.success(f"API Response: {result.text}")
        except Exception as e:
            st.error(f"API Error: {str(e)}")
    
    # Show mode
    st.subheader("Current Mode")
    try:
        mode = st.query_params.get("mode", "client")
    except:
        mode = "client"
    st.write(f"Mode: {mode}")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()