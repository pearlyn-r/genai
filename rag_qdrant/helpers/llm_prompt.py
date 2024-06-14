# helpers/llm_prompt.py

import streamlit as st
from config.constants import OLLAMA_MODEL
from helpers.qdrant_client import search_qdrant

def ollama_chat(input, system_message, ollama_model, conversation_history, client):
    print("Called: ollama_chat")
    
    # Get relevant context from Qdrant
    search_result = search_qdrant(input, ollama_model, "demo")
    
    context_str = "relevant context is \n\n".join(result.payload['text'] for result in search_result) if search_result else "No relevant context found."
    
    #user_input_with_context = input + "\n\nRelevant Context:\n" + context_str 
    conversation_history.append({"role": "user", "content": input})
    
    messages = [{"role": "system", "content": system_message}, *conversation_history]
    messages.append({"role": "user", "content": context_str})
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=2000,
    )
    assistant_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_response})
    return assistant_response
