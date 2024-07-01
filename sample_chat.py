import streamlit as st
import numpy as np

import random
import time

st.title("Sample chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    with st.chat_message("assistant"):
        st.markdown(response)
        st.bar_chart(np.random.randn(30, 3))
        st.write("Hello Human ")
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})