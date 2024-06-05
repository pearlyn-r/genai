# Mutual Fund Advisor with Llama3

This project integrates Automatic Speech Recognition (ASR) and Large Language Models (LLMs) to create a conversational AI system that assists users with mutual fund advice. The system uses Whisper for speech recognition and LLaMA 3, accessed via the Ollama API, for generating responses.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)

## Introduction

The Mutual Fund Advisor project leverages state-of-the-art AI technologies to provide users with personalized mutual fund recommendations. Users can interact with the system using both voice and text input, allowing for a more natural and intuitive user experience.

## Features

- **Voice and Text Input:** Users can ask questions using voice or text.
- **Contextual Understanding:** The system retrieves relevant information from a pre-loaded vault of documents.
- **Conversational AI:** Uses LLaMA 3 to generate human-like responses.
- **Real-time Transcription:** Converts voice input to text using Whisper.

## Technologies Used

- **Python:** For the core logic and application structure.
- **Whisper (OpenAI):** For automatic speech recognition.
- **Ollama for LLaMA 3:** For natural language understanding and response generation.
- **Streamlit:** For creating the web application interface.
- **Torch:** For handling embeddings and cosine similarity computations.

## Setup Instructions

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/pearlyn-r/genai.git
    cd genai/rag_for_mutual_funds
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Download the LLaMA 3 Model:**
    Make sure to have installed the Ollama application (https://github.com/ollama/ollama?tab=readme-ov-file). Pull the model data onto your local machine:
    ```bash
    ollama pull llama3
    ```

4. **Prepare the Vault:**
    Ensure you have a `vault.txt` file in the same directory as the script. This file should contain the content you want the system to use for generating relevant context.

## Usage

1. **Run the Application:**
    ```bash
    streamlit run rag_conv.py
    ```

2. **Interacting with the System:**
    - Use the microphone button to record your voice input.
    - The system will transcribe the audio and generate a response based on the transcribed text and relevant context from the vault.
    - Alternatively, you can type your query in the text input box and submit it.

3. **Understanding the Output:**
    - The assistant will provide responses based on the user input and the context retrieved from the vault documents.
    - The conversation history is displayed for reference.


