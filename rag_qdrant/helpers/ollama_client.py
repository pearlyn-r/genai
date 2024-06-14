from openai import OpenAI
def initialize_ollama_client(base_url, api_key):
    return OpenAI(
        base_url=base_url,
        api_key=api_key
    )
