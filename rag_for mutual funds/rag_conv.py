import streamlit as st
import torch
import ollama
import os
import json
from openai import OpenAI



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

def ollama_chat(user_input, system_message, vault_embeddings, vault_content, ollama_model, conversation_history):
    relevant_context = get_relevant_context(user_input, vault_embeddings, vault_content)
    if relevant_context:
        context_str = "\n\n".join(relevant_context)
        st.write("Context Pulled from Documents: \n\n" )
    else:
        st.write("No relevant context found.")

    if relevant_context:
        user_input_with_context = user_input + "\n\nRelevant Context:\n" + context_str

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
st.title("Mutual Fund Advisor with Llama3")

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
    st.session_state.system_message = """You are a helpful assistant and your primary role is that of a financial advisor to learn about the users financial profile 
    and preferences and  bring in extra relevant information to the user query from outside the given context.Extract relevant information from the text provided to
    Ultimately helping the user to make a decision of what to invest."""

# Display conversation history
if st.session_state.conversation_history:
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            st.write(f"**User:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.write(f"**Assistant:** {msg['content']}")

# Input for user query (always at the bottom)
user_input = st.text_input("Ask a query about your documents", key="user_input")

if st.button("Submit"):
    if user_input:
        response = ollama_chat(user_input, st.session_state.system_message, vault_embeddings_tensor, vault_content, ollama_model, st.session_state.conversation_history)
        
        st.experimental_rerun()
    else:
        st.write("Please enter a query.")
