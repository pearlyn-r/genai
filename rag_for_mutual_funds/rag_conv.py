import streamlit as st
import torch
import ollama
import os
import json
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
import whisper

def initialize_whisper_model():
    return whisper.load_model("base")

def initialize_ollama_client(base_url, api_key):
    return OpenAI(
        base_url=base_url,
        api_key=api_key
    )

def load_vault_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as vault_file:
            return vault_file.readlines()
    else:
        return None

def generate_vault_embeddings(vault_content, ollama_model):
    vault_embeddings = []
    for content in vault_content:
        response = ollama.embeddings(model=ollama_model, prompt=content)
        vault_embeddings.append(response["embedding"])
    return torch.tensor(vault_embeddings)

# Function to get relevant context from the vault based on user input
def get_relevant_context(user_input, vault_embeddings, vault_content, top_k=3):
    if vault_embeddings.nelement() == 0:  # Check if the tensor has any elements
        return []
    # Encode the user input
    input_embedding = ollama.embeddings(model='llama3', prompt=user_input)["embedding"]

    # Compute cosine similarity between the input and vault embeddings
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)

    # Adjust top_k if it's greater than the number of available scores
    top_k = min(top_k, len(cos_scores))
    # Sort the scores and get the top-k indices
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    
    # Get the corresponding context from the vault
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context

def ollama_chat(input, system_message, vault_embeddings, vault_content, ollama_model, conversation_history, client):
    relevant_context = get_relevant_context(input, vault_embeddings, vault_content)
    context_str = "\n\n".join(relevant_context) if relevant_context else "No relevant context found."
    st.write(f"Context Pulled from Documents: \n\n{context_str}" if relevant_context else context_str)

    user_input_with_context = input + "\n\nRelevant Context:\n" + context_str if relevant_context else input
    conversation_history.append({"role": "user", "content": user_input_with_context})
    
    messages = [{"role": "system", "content": system_message}, *conversation_history]
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=2000,
    )
    assistant_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_response})
    return assistant_response
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from streamlit_float import float_init

# Initialize
float_init()
whisper_model = initialize_whisper_model()
base_url = 'http://localhost:11434/v1'
api_key = 'llama3'
ollama_model = 'llama3'
client = initialize_ollama_client(base_url, api_key)
vault_content = load_vault_content("vault.txt")
vault_embeddings_tensor = generate_vault_embeddings(vault_content, ollama_model) if vault_content else torch.tensor([])

# Initialize conversation history and system message in session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'system_message' not in st.session_state:
    st.session_state.system_message = """You are a helpful assistant and your primary role is that of a financial advisor to learn about the user's financial profile 
and preferences and bring in extra relevant information to the user query from outside the given context. Extract relevant information from the text provided to
ultimately help the user make a decision on what to invest by making normal conversation with them Your role is to have a natural conversation with the user, understand their financial situation and preferences,
and provide tailored advice and suggestions for potential investments or financial strategies."""

def display_conversation_history():
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            st.write(f"**User:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.write(f"**Assistant:** {msg['content']}")

def handle_audio_input(audio_bytes):
    if audio_bytes:
        with st.spinner("Transcribing..."):
            webm_file_path = "temp_audio.mp3"
            with open(webm_file_path, "wb") as f:
                f.write(audio_bytes)
            result = whisper_model.transcribe(webm_file_path)
            os.remove(webm_file_path)
            return result['text'] if result else None
    return None

def handle_text_input(user_input):
    if user_input:
        response = ollama_chat(user_input, st.session_state.system_message, vault_embeddings_tensor, vault_content, ollama_model, st.session_state.conversation_history, client)
        st.write(f"**Assistant:** {response}")
        user_input=None
        st.experimental_rerun()
    else:
        st.write("Please enter a query.")

def main():
    st.title("Mutual Fund Advisor with Llama3")
    footer_container = st.container()
    with footer_container:
        audio_bytes = audio_recorder()

    display_conversation_history()

    if audio_bytes:
        transcript = handle_audio_input(audio_bytes)
        if transcript:
            st.write(f"**Transcribed Text:** {transcript}")
            response = ollama_chat(transcript, st.session_state.system_message, vault_embeddings_tensor, vault_content, ollama_model, st.session_state.conversation_history, client)
            st.write(f"**Assistant:** {response}")
            transcript=None
        footer_container.float("bottom: 0rem;")
    user_input = st.text_input("Ask a query about your documents", key="user_input")
    if st.button("Submit", key="submit_button"):
        handle_text_input(user_input)
    footer_container.write("")

if __name__ == "__main__":
    main()
