# Voice-Interactive Stock and Mutual Fund Advisor

Welcome to the Voice-Interactive Stock and Mutual Fund Advisor! This project aims to create a more interactive and user-friendly environment by allowing users to input messages via voice commands. The system utilizes a large language model (LLM) to ask relevant questions and recommend stocks or mutual funds based on the user's responses.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Usage](#usage)

## Introduction

The Voice-Interactive Stock and Mutual Fund Advisor is designed to simplify the process of finding suitable investment options by using voice input. Users can speak their queries, and the system will process these inputs to provide personalized investment advice.

## Features

- **Voice Input:** Users can interact with the system using their voice.
- **Interactive Q&A:** The system asks relevant questions to understand the user's preferences and risk tolerance.
- **Personalized Recommendations:** Based on the user's responses, the system recommends appropriate stocks or mutual funds.
- **User-Friendly Interface:** Easy-to-use interface designed for seamless interaction.

## Technologies Used

- **Python:** For the core logic and interaction with the LLM.
- **Whisper:** For capturing and processing voice inputs.
- **Ollama for LLaMA3:** For natural language understanding and generating questions.
- **Finance API:** To fetch real-time stock and mutual fund data.

## Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/voice-interactive-advisor.git
    cd voice-interactive-advisor
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Download the LLAMA 3 Model Locally:
    To use LLAMA 3 in your project, you need to pull the model data onto your local machine. Run the following command in your terminal:
    ```bash
    ollama pull llama3
    ```


4. Run the application using Streamlit:
    ```bash
    streamlit run voicellm.py
    ```

6. Follow the on-screen instructions to interact with the system using your voice.
