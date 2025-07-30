import streamlit as st
from utils.ai_integration import initialize_ai, AI_AVAILABLE
from utils.session_state import initialize_session_state
from pages.calculator_page import show_calculator_page
from pages.goal_tracker_page import show_goal_tracker_page
from pages.chatbot_page import show_chatbot_page

# Page configuration
st.set_page_config(
    page_title="Fynstra – Financial Health Index", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize everything
initialize_ai()
initialize_session_state()

# Main App Header
st.title("⌧ Fynstra")
st.markdown("### AI-Powered Financial Health Platform for Filipinos")

# Show AI status
if AI_AVAILABLE:
    st.success("🤖 FYNyx AI is online and ready to help!")
else:
    st.warning("🤖 FYNyx AI is in basic mode. Install google-generativeai for full AI features.")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a feature:", [
    "Financial Health Calculator", 
    "Goal Tracker", 
    "FYNyx Chatbot"
])

# Route to appropriate page
if page == "Financial Health Calculator":
    show_calculator_page()
elif page == "Goal Tracker":
    show_goal_tracker_page()
elif page == "FYNyx Chatbot":
    show_chatbot_page()

# Footer
st.markdown("---")
st.markdown("**Fynstra AI** - Empowering Filipinos to **F**orecast, **Y**ield, and **N**avigate their financial future with confidence.")
st.markdown("*Developed by Team HI-4requency for DataWave 2025*")
