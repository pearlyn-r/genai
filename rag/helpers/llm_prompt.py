import streamlit as st
from config.constants import OLLAMA_MODEL
from helpers.embeddings import get_relevant_context

def ollama_chat(input, system_message, vault_content, ollama_model, conversation_history, client):
    print("Called: ollama_chat")
    
    context_str = "\n\n".join(vault_content) if vault_content else "No relevant context found."
    #st.write(f"Context Pulled from Documents: \n\n{context_str}" )

    user_input_with_context = input + "\n\nRelevant Context:\n" + context_str 
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
