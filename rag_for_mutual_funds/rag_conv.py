import streamlit as st
import torch
import ollama
import os
import json
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
import whisper

# Load Whisper model
whisper_model = whisper.load_model("base")

# Float feature initialization
float_init()
# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()


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

def ollama_chat(input, system_message, vault_embeddings, vault_content, ollama_model, conversation_history):
    relevant_context = get_relevant_context(input, vault_embeddings, vault_content)
    if relevant_context:
        context_str = "\n\n".join(relevant_context)
        st.write("Context Pulled from Documents: \n\n" )
    else:
        st.write("No relevant context found.")

    if relevant_context:
        user_input_with_context = input + "\n\nRelevant Context:\n" + context_str

    conversation_history.append({"role": "user", "content": user_input_with_context})

    messages = [
        {"role": "system", "content": system_message},
        *conversation_history
    ]

    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=2000,
    )

    assistant_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_response})

    return assistant_response

# Streamlit app
st.title("Mutual Fund Advisor withs Llama3")

# Configuration for the Ollama API client
base_url = 'http://localhost:11434/v1'
api_key = 'llama3'
ollama_model = 'llama3'

# Initialize the OpenAI client
client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

# Load the vault content
vault_content = []
if os.path.exists("vault.txt"):
    with open("vault.txt", "r", encoding='utf-8') as vault_file:
        vault_content = vault_file.readlines()
else:
    st.error("vault.txt file not found. Please make sure the file is in the same directory as the script.")

# Generate embeddings for the vault content using Ollama
vault_embeddings = []
if vault_content:
    for content in vault_content:
        response = ollama.embeddings(model=ollama_model, prompt=content)
        vault_embeddings.append(response["embedding"])

    # Convert to tensor
    vault_embeddings_tensor = torch.tensor(vault_embeddings)

# Initialize conversation history and system message in session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'system_message' not in st.session_state:
    st.session_state.system_message = """You are a helpful assistant and your primary role is that of a financial advisor to learn about the user's financial profile 
and preferences and bring in extra relevant information to the user query from outside the given context. Extract relevant information from the text provided to
ultimately help the user make a decision on what to invest by making normal conversation with them Your role is to have a natural conversation with the user, understand their financial situation and preferences,
and provide tailored advice and suggestions for potential investments or financial strategies."""

# Display conversation history
if st.session_state.conversation_history:
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            st.write(f"**User:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.write(f"**Assistant:** {msg['content']}")


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

            # Print the transcribed text
            st.write(f"**Transcribed Text:** {transcript}")

            # Call ollama_chat with the transcribed text
            response = ollama_chat(transcript, st.session_state.system_message, vault_embeddings_tensor, vault_content, ollama_model, st.session_state.conversation_history)
            st.write(f"**Assistant:** {response}")

            
            footer_container.float("bottom: 0rem;")

# Input for text query (always at the bottom)
user_input = st.text_input("Ask a query about your documents", key="user_input")

if st.button("Submit", key="submit_button"):
    if user_input:
        response = ollama_chat(user_input, st.session_state.system_message, vault_embeddings_tensor, vault_content, ollama_model, st.session_state.conversation_history)
        st.write(f"**Assistant:** {response}")
    
        st.experimental_rerun()
        
    else:
        st.write("Please enter a query.")

# Ensure the footer container is always displayed
footer_container.write("")
