import streamlit as st
from config.constants import OLLAMA_MODEL
from helpers.qdrant_client import search_qdrant

def ollama_chat(input, system_message, ollama_model, conversation_history, client):
    print("Called: ollama_chat")
    
    
    if len(st.session_state.questions_answered) < 4:
        # in the question-asking phase
        messages = [{"role": "system", "content": system_message}, *conversation_history]
        messages.append({"role": "user", "content": input})
        
        response = client.chat.completions.create(
            model=ollama_model,
            messages=messages,
            max_tokens=3000,
        )
        assistant_response = response.choices[0].message.content
        
        if "Next question" in assistant_response or "Based on your answers" in assistant_response:
            st.session_state.questions_answered.add(st.session_state.current_question)
            st.session_state.current_question = len(st.session_state.questions_answered) + 1
            print(st.session_state.questions_answered)
        
        # answered the 4th question, immediately switch to recommendation phase
        if len(st.session_state.questions_answered) == 4:
            search_result = search_qdrant(input, ollama_model, "demo")
            context_str = "Relevant mutual fund data:\n" + "\n".join(result.payload['text'] for result in search_result) if search_result else "No relevant mutual fund data found."
            messages.append({"role": "user", "content": f"\n\n{context_str}\n\nBased on this profile and the provided mutual fund data, recommend two specific investment options."})
            return ollama_chat(input, system_message, ollama_model, conversation_history, client)
        
    else:
        #  finished asking questions, now include relevant context
        search_result = search_qdrant(input, ollama_model, "demo")
        context_str = "Relevant mutual fund data:\n" + "\n".join(result.payload['text'] for result in search_result) if search_result else "No relevant mutual fund data found."
        
        # Prepare a summary of user's answers
        user_profile = summarize_user_profile(conversation_history)
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"User Profile:\n{user_profile}\n\n{context_str}\n\nBased on this profile and the provided mutual fund data, recommend two specific investment options."}
        ]
        
        response = client.chat.completions.create(
            model=ollama_model,
            messages=messages,
            max_tokens=3000,
        )
        assistant_response = response.choices[0].message.content
    
    return assistant_response

def summarize_user_profile(conversation_history):
    # Extract user's answers from the conversation history
    user_answers = [msg["content"] for msg in conversation_history if msg["role"] == "user"][-4:]
    return "\n".join(f"Q{i+1}: {answer}" for i, answer in enumerate(user_answers))