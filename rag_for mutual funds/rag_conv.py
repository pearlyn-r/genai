import streamlit as st
import torch
import ollama
import os
import json
from openai import OpenAI

# Function to get relevant context from the vault based on user input
def get_relevant_context(rewritten_input, vault_embeddings, vault_content, top_k=3):
    if vault_embeddings.nelement() == 0:  # Check if the tensor has any elements
        return []
    # Encode the rewritten input
    input_embedding = ollama.embeddings(model='llama3', prompt=rewritten_input)["embedding"]

    # Compute cosine similarity between the input and vault embeddings
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)

    # Adjust top_k if it's greater than the number of available scores
    top_k = min(top_k, len(cos_scores))
    # Sort the scores and get the top-k indices
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    
    # Get the corresponding context from the vault
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context

def rewrite_query(user_input_json, conversation_history, ollama_model):
    user_input = json.loads(user_input_json)["Query"]
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-2:]])
    prompt = f"""Rewrite the following query by incorporating relevant context from the conversation history.
    The rewritten query should:

    - Preserve the core intent and meaning of the original query
    - Expand and clarify the query to make it more specific and informative for retrieving relevant context.
    - Avoid introducing new topics or queries that deviate from the original query
    - Ask the user questions related to the original query that are related and might help you reach a more informed decision, hence act as a financial advisor to understand them
    - DONT EVER ANSWER the Original query, but instead focus on rephrasing and expanding it into a new query

    Return ONLY the rewritten query text, without any additional formatting or explanations.

    Conversation History:
    {context}

    Original query: [{user_input}]

    Rewritten query: 
    """
    response = client.chat.completions.create(
        model=ollama_model,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=200,
        n=1,
        temperature=0.1,
    )
    rewritten_query = response.choices[0].message.content.strip()
    return json.dumps({"Rewritten Query": rewritten_query})

def ollama_chat(user_input, system_message, vault_embeddings, vault_content, ollama_model, conversation_history):
    if len(conversation_history) > 1:
        query_json = {
            "Query": user_input,
            "Rewritten Query": ""
        }
        rewritten_query_json = rewrite_query(json.dumps(query_json), conversation_history, ollama_model)
        rewritten_query_data = json.loads(rewritten_query_json)
        rewritten_query = rewritten_query_data["Rewritten Query"]
    else:
        rewritten_query = user_input

    relevant_context = get_relevant_context(rewritten_query, vault_embeddings, vault_content)

    user_input_with_context = rewritten_query
    if relevant_context:
        context_str = "\n\n".join(relevant_context)
        user_input_with_context = rewritten_query + "\n\nRelevant Context:\n" + context_str

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
st.title("Ollama Chat Interface")

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
    st.session_state.system_message = "You are a helpful assistant that is an expert at extracting the most useful information from a given text. Your primary role is that of a financial advisor. Also bring in extra relevant information to the user query from outside the given context."

# Initialize state for rewritten query and response input
if 'rewritten_query' not in st.session_state:
    st.session_state.rewritten_query = None

# Display conversation history
if st.session_state.conversation_history:
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            st.write(f"**User:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.write(f"**Assistant:** {msg['content']}")

if st.session_state.rewritten_query is None:
    # Input for user query (always at the bottom)
    user_input = st.text_input("Ask a query about your documents", key="user_input")

    if st.button("Submit"):
        if user_input:
            # Rewrite the query
            query_json = {
                "Query": user_input,
                "Rewritten Query": ""
            }
            rewritten_query_json = rewrite_query(json.dumps(query_json), st.session_state.conversation_history, ollama_model)
            rewritten_query_data = json.loads(rewritten_query_json)
            st.session_state.rewritten_query = rewritten_query_data["Rewritten Query"]
            st.experimental_rerun()  # Rerun to prompt for second input
        else:
            st.write("Please enter a query.")
else:
    # Show the rewritten query and ask for user input
    st.write("Rewritten Query: " + st.session_state.rewritten_query)
    user_response = st.text_input("Your response to the rewritten query", key="user_response")

    if st.button("Submit Response"):
        if user_response:
            # Generate response based on user's input
            response = ollama_chat(user_response, st.session_state.system_message, vault_embeddings_tensor, vault_content, ollama_model, st.session_state.conversation_history)
            st.session_state.conversation_history.append({"role": "user", "content": user_response})
            st.write("**Assistant:** " + response)  # Display assistant response only once
            st.session_state.rewritten_query = None  # Reset the rewritten query state
        else:
            st.write("Please enter a response.")
