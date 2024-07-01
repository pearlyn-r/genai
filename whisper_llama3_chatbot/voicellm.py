import ollama
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
import os
# Import Whisper for speech recognition
import whisper

# Load Whisper model
whisper_model = whisper.load_model("base")

# Float feature initialization
float_init()

st.title("Transcribe Speech with Whisper")

# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

# Initialize chat messages if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat message history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

# Function to generate response from the chatbot
def generate_response(transcript):
    response = ollama.chat(model='llama3', stream=True, messages=st.session_state.messages)
    full_message = ""
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        full_message += token
        yield token
    return full_message

# Transcribe audio if recording is available
if audio_bytes:
    # Write the audio bytes to a file
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        # Transcribe audio using Whisper
        result = whisper_model.transcribe(webm_file_path)
        if result:
            transcript = result['text']
            os.remove(webm_file_path)

            # Display transcript in chat input box
            st.text_input("You:", value=transcript)

            # Add transcript to session state messages
            st.session_state.messages.append({"role": "user", "content": transcript})
            st.chat_message("user", avatar="🧑‍💻").write(transcript)

            # Generate response from chatbot
            assistant_response = ''.join(token for token in generate_response(transcript))

            # Display assistant response and update session state messages
            st.write(st.chat_message("assistant", avatar="🤖").write(assistant_response))
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})


            footer_container.float("bottom: 0rem;")
