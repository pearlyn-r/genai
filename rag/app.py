import streamlit as st
from audio_recorder_streamlit import audio_recorder
from streamlit_float import float_init
from config.constants import BASE_URL, API_KEY, OLLAMA_MODEL
from audio.whispermodel import initialize_whisper_model
from helpers.ollama_client import initialize_ollama_client
from helpers.embeddings import load_vault_content
from helpers.llm_prompt import ollama_chat
from audio.audio_input import handle_audio_input
from config.session_state import initialize_session_state
import torch

# Initialize
float_init()
initialize_session_state()
whisper_model = initialize_whisper_model()
client = initialize_ollama_client(BASE_URL, API_KEY)
vault_content = load_vault_content("data/vault.txt")

def display_conversation_history():
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            st.write(f"**User:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.write(f"**Assistant:** {msg['content']}")

def main():
    st.title("Mutual Fund Advisor with Llama3")
    footer_container = st.container()
    with footer_container:
        audio_bytes = audio_recorder()
        # Reset audio_processed flag if new audio is recorded
        if audio_bytes:
            st.session_state.audio_processed = False

    display_conversation_history()

    if audio_bytes and not st.session_state.audio_processed:
        transcript = handle_audio_input(audio_bytes, whisper_model)
        if transcript:
            st.write(f"**Transcribed Text:** {transcript}")
            # Store user input in conversation history
            st.session_state.conversation_history.append({"role": "user", "content": transcript})

            response = ollama_chat(transcript, st.session_state.system_message, vault_content, OLLAMA_MODEL, st.session_state.conversation_history, client)
            st.write(f"**Assistant:** {response}")

            # Store assistant response in conversation history
            st.session_state.conversation_history.append({"role": "assistant", "content": response})

            st.session_state.audio_processed = True

        footer_container.float("bottom: 0rem;")

    footer_container.write("")
if __name__ == "__main__":
    main()    
