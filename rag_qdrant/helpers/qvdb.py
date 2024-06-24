import torch
import ollama
import os
import json
import re
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct

# Qdrant client setup
QDRANT_API_KEY = "sUyiBek7WYNcIJW1COu7RaZ9DOiWIAzZ4zhJPcTjCJU-kmXZZgBpNQ"
QDRANT_URL = (
    'https://57cf6c2f-36fb-4af3-8728-e6f997051d5d.us-east4-0.gcp.cloud.qdrant.io:6333' 
)

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Recreate the Qdrant collection
qdrant_client.recreate_collection(
    collection_name="demo",
    vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
)

def load_vault_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as vault_file:
            return vault_file.read()
    else:
        return None

def clean_json_string(json_string):
    # Remove control characters
    json_string = re.sub(r'[\x00-\x1F\x7F]', '', json_string)
    return json_string

def get_embedding(text, ollama_model):
    response = ollama.embeddings(model=ollama_model, prompt=text)
    return response["embedding"]

def chunk_content(full_text, chunk_size=2000):
    chunks = []
    while len(full_text) > chunk_size:
        last_period_index = full_text[:chunk_size].rfind('}')
        if last_period_index == -1:
            last_period_index = chunk_size
        chunks.append(full_text[:last_period_index+1])
        full_text = full_text[last_period_index+1:].strip()
    chunks.append(full_text)
    return chunks

def generate_embeddings_df(vault_content, ollama_model):
    data = []
    try:
        cleaned_content = clean_json_string(vault_content)
        chunks = chunk_content(cleaned_content)
        for idx, chunk in enumerate(chunks):
            try:
                embedding = get_embedding(chunk, ollama_model)
                data.append({
                    "id": idx,
                    "chunk": chunk,
                    "embedding": embedding
                })
            except Exception as e:
                print(f"Error generating embedding for chunk: {chunk}, Error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Cleaned Content: {cleaned_content}")
    except Exception as e:
        print(f"Processing failed: {e}")
        print(f"Content: {vault_content}")
    return pd.DataFrame(data)

def upsert_to_qdrant(full_text, ollama_model, collection_name, client):
    # Clean and chunk the content
    cleaned_text = clean_json_string(full_text)
    chunks = chunk_content(cleaned_text)

    # Generate embeddings and prepare points for Qdrant
    points = []
    for i, chunk in enumerate(chunks, start=1):
        embeddings = get_embedding(chunk, ollama_model)
        points.append(PointStruct(id=i, vector=embeddings, payload={"text": chunk}))

    # Upsert points into Qdrant
    operation_info = client.upsert(
        collection_name=collection_name,
        wait=True,
        points=points
    )

    return operation_info

def get_embedding_for_query(user_input, ollama_model):
    response = ollama.embeddings(model=ollama_model, prompt=user_input)
    return response["embedding"]

def create_answer_with_context(query):
    # Generate embeddings for the input query
    embeddings = get_embedding_for_query(query, "mxbai-embed-large")

    # Perform search using Qdrant with the query vector (embeddings)
    search_result = qdrant_client.search(
        collection_name="demo",
        query_vector=embeddings,
        limit=3
    )

    # Print the search results
    print("Search Results from Vector Database:")
    for result in search_result:
        print(result.payload['text'])

    # Build the prompt with the context retrieved from Qdrant
    prompt = """You are a helpful assistant and your primary role is that of a financial advisor to learn about the user's financial profile 
and preferences and bring in extra relevant information to the user query from outside the given context. Extract relevant information from the text provided to
ultimately help the user make a decision on what to invest by making normal conversation with them. Your role is to have a natural conversation with the user, understand their financial situation and preferences,
and provide tailored advice and suggestions for potential investments or financial strategies.\n"""
    for result in search_result:
        prompt += result.payload['text'] + "\n---\n"
    prompt += "Question:" + query + "\n---\n" + "Answer:"

    # Generate response using Ollama's llama3 model
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Check for errors in the response and handle them
    if 'message' not in response:
        raise ValueError(f"Unexpected response format: {response}")

    return response['message']['content']

# Main function
def main(collection_name):
    file_path = "data/vault.txt"
    vault_content = load_vault_content(file_path)

    if vault_content:
        print("Vault Content:")
        print(vault_content)

        # Upsert the embeddings into Qdrant
        operation_info = upsert_to_qdrant(vault_content, "mxbai-embed-large", collection_name, qdrant_client)
        print("Upsert Operation Info:")
        print(operation_info)
        user_input = "recommend a query with max beta"
        answer = create_answer_with_context(user_input)
        print("Answer:")
        print(answer)
    else:
        print("File not found or is empty.")

# Example usage
if __name__ == "__main__":
    collection_name = 'demo'
    main(collection_name)
