
import streamlit as st
def ollama_chat(input, system_message, vault_content, ollama_model, conversation_history, client):
    print("Called: ollama_chat")
    
    context_str = "\n\n".join(vault_content) if vault_content else "No relevant context found."
    
    # Combine user input with context for the model
    #user_input_with_context = input + "\n\nRelevant Context:\n" + context_str
    # Append the plain user input to the conversation history
    #conversation_history.append({"role": "user", "content": input})

    # Check for consecutive duplicate user inputs for the last two entries   
    # Prepare messages with system message and conversation history (excluding context)
    messages = [{"role": "system", "content": system_message}, *conversation_history]
    messages.append({"role": "user", "content": context_str})

    # Generate response from the model
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=2000,
    )
    
    # Extract and append the assistant response to the conversation history
    assistant_response = response.choices[0].message.content
    #conversation_history.append({"role": "assistant", "content": assistant_response})
    return assistant_response
