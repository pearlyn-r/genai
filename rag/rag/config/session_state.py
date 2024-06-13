import streamlit as st
from config.constants import SYSTEM_MESSAGE

# Initialize session state
def initialize_session_state():
    print("Called: initialize_session_state")
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    if 'system_message' not in st.session_state:
        st.session_state.system_message = SYSTEM_MESSAGE

    if 'audio_processed' not in st.session_state:
        st.session_state.audio_processed = False

    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

