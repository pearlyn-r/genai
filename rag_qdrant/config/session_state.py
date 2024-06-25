import streamlit as st
from config.constants import SYSTEM_MESSAGE

def initialize_session_state():
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'system_message' not in st.session_state:
        st.session_state.system_message = SYSTEM_MESSAGE
    if 'audio_processed' not in st.session_state:
        st.session_state.audio_processed = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 1
    if 'questions_answered' not in st.session_state:
        st.session_state.questions_answered = set()
