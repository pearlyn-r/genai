import os
import streamlit as st

def handle_audio_input(audio_bytes, whisper_model):
    # print("Called: handle_audio_input")
    # if audio_bytes:
    #     with st.spinner("Transcribing..."):
    #         webm_file_path = "temp_audio.mp3"
    #         with open(webm_file_path, "wb") as f:
    #             f.write(audio_bytes)
    #         result = whisper_model.transcribe(webm_file_path)
    #         os.remove(webm_file_path)
    #         st.session_state.audio_bytes = None
    #         audio_bytes=None
    #         return result['text'] if result else None

    return audio_bytes
