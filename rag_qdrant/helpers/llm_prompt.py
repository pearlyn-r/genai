# helpers/llm_prompt.py

import streamlit as st
from config.constants import OLLAMA_MODEL
from helpers.qdrant_client import search_qdrant

def ollama_chat(input, system_message, ollama_model, conversation_history, client):
    print("Called: ollama_chat")
    
    if st.session_state.question_count < 4:
        # We're still in the question-asking phase
        st.session_state.question_count += 1
        print(st.session_state.question_count)
        messages = [{"role": "system", "content": system_message}, *conversation_history]
        messages.append({"role": "user", "content": input})
    else:
        # Normal RAG process
        search_result = search_qdrant(input, ollama_model, "demo")
        context_str = "relevant context is \n\n".join(result.payload['text'] for result in search_result) if search_result else "No relevant context found."
        messages = [{"role": "system", "content": system_message}, *conversation_history]
        messages.append({"role": "user", "content": input + "\n\nRelevant Context:\n" + context_str})
    
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=3000,
    )
    assistant_response = response.choices[0].message.content
    
    return assistant_response
