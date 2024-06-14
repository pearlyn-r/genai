
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from streamlit_float import float_init
from config.constants import BASE_URL, API_KEY, OLLAMA_MODEL
from audio.whispermodel import initialize_whisper_model
from helpers.ollama_client import initialize_ollama_client
from helpers.embeddings import  generate_vault_embeddings
from helpers.llm_prompt import ollama_chat
from audio.audio_input import handle_audio_input
from config.session_state import initialize_session_state

# Initialize
float_init()
initialize_session_state()
whisper_model = initialize_whisper_model()
client = initialize_ollama_client(BASE_URL, API_KEY)

# Generate embeddings and upsert to Qdrant you need to run the underlying line if u are running it for the first time
#generate_vault_embeddings("data/vault.txt", OLLAMA_MODEL, "demo")

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
        if audio_bytes:
            st.session_state.audio_processed = False

    display_conversation_history()

    if audio_bytes and not st.session_state.audio_processed:
        transcript = handle_audio_input(audio_bytes, whisper_model)
        if transcript:
            # Display user's transcribed text
            st.write(f"**User:** {transcript}")
            st.session_state.conversation_history.append({"role": "user", "content": transcript})

            # Process with assistant's response
            response = ollama_chat(transcript, st.session_state.system_message, OLLAMA_MODEL, st.session_state.conversation_history, client)
            st.write(f"**Assistant:** {response}")
            st.session_state.conversation_history.append({"role": "assistant", "content": response})

            st.session_state.audio_processed = True
            
        footer_container.float("bottom: 0rem;")

    footer_container.write("")


if __name__ == "__main__":
    main()
