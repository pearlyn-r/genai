# Mutual Fund Advisor with Llama3

This project integrates Automatic Speech Recognition (ASR) and Large Language Models (LLMs) to create a conversational AI system that assists users with mutual fund advice. The system uses Whisper for speech recognition and LLaMA 3, accessed via the Ollama API, for generating responses.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Key Buisness Needs](#key_buisness_needs)
- [Technologies Used](#technologies-used)
- [Hardware Requirements](#hardware-requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)

## Introduction

The Mutual Fund Advisor project leverages state-of-the-art AI technologies to provide users with personalized mutual fund recommendations. Users can interact with the system using both voice and text input, allowing for a more natural and intuitive user experience.

## Features

- **Voice and Text Input:** Users can ask questions using voice or text.
- **Contextual Understanding:** The system retrieves relevant information from a pre-loaded vault of documents.
- **Conversational AI:** Uses LLaMA 3 to generate human-like responses.
- **Real-time Transcription:** Converts voice input to text using Whisper.

## Key Business Needs

 ####  Enhanced Customer Service 
- **24/7 Availability**: Provides round-the-clock assistance, ensuring access to financial advice anytime.
- **Instant Response**: Reduces wait times with immediate responses to customer queries.

 #### Personalized Financial Advice
- **Tailored Recommendations**: Offers personalized investment suggestions based on individual profiles and preferences.
- **Contextual Assistance**: Uses relevant information from documents and past interactions for accurate advice.

 #### Increased Operational Efficiency
- **Reduced Workload for Human Advisors**: Handles routine inquiries, allowing human advisors to focus on complex tasks.
- **Scalability**: Manages unlimited customer interactions simultaneously, scaling advisory services efficiently.

 #### Customer Engagement and Retention
- **Improved Interaction Quality**: Engages customers with conversational AI, enhancing the experience.
- **Proactive Engagement**: Alerts customers to timely investment opportunities and market trends based on their profiles.

#### Data-Driven Insights
- **Customer Behavior Analysis**: Analyzes interactions to understand customer preferences and pain points.
- **Market Trends Identification**: Aggregates data to identify broader market trends and customer sentiment.

#### Competitive Advantage
- **Innovation Leadership**: Positions the bank as a leader in AI technology, attracting tech-savvy customers.
- **Differentiation**: Offers a unique voice-activated financial advisor, setting the bank apart from competitors.


## Technologies Used

- **Python:** For the core logic and application structure.
- **Whisper (OpenAI):** For automatic speech recognition.
- **Ollama for LLaMA 3:** For natural language understanding and response generation.
- **Streamlit:** For creating the web application interface.
- **Torch:** For handling embeddings and cosine similarity computations.

## Hardware Pre-requisites: A recommended system configuration for installing Ollama is given below.

- **CPU**: Any modern CPU with at least 4 cores recommended for running smaller models. For running 13B models, CPU with at least 8 cores is recommended. GPU is optional for Ollama, but if available can improve the performance drastically.
- **RAM**: At least 8 GB of RAM to run the 7B models, 16 GB to run the 13B models, and 32 GB to run the 33B models.(i ran 7B model with 16gb RAM )
- **Disk Capacity**: Recommend at least 12 GB of disk space available, to install Ollama and the base models. Additional space will be required if more models are planned to be installed.

## Setup Instructions
It requires the command-line tool ffmpeg to be installed on your system, which is available from most package managers:
```bash
    # on Ubuntu or Debian
    sudo apt update && sudo apt install ffmpeg
    
    # on Arch Linux
    sudo pacman -S ffmpeg
    
    # on MacOS using Homebrew (https://brew.sh/)
    brew install ffmpeg
    
    # on Windows using Chocolatey (https://chocolatey.org/)
    choco install ffmpeg
    
    # on Windows using Scoop (https://scoop.sh/)
    scoop install ffmpeg
```
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


