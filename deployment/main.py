"""
Alternate entry point for Streamlit deployment
Some configurations prefer main.py over streamlit_app.py
"""

from streamlit_app import main

if __name__ == "__main__":
    main()