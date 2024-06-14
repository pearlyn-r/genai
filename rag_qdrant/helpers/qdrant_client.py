
import re
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
import ollama
from config.secrets import QDRANT_API_KEY, QDRANT_URL

# Qdrant client setup
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def recreate_collection(collection_name, vector_size=4096):
    qdrant_client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
    )

def clean_json_string(json_string):
    json_string = re.sub(r'[\x00-\x1F\x7F]', '', json_string)
    return json_string

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

def get_embedding(text, ollama_model):
    response = ollama.embeddings(model=ollama_model, prompt=text)
    return response["embedding"]

def upsert_to_qdrant(full_text, ollama_model, collection_name):
    cleaned_text = clean_json_string(full_text)
    chunks = chunk_content(cleaned_text)
    points = []
    for i, chunk in enumerate(chunks, start=1):
        embeddings = get_embedding(chunk, ollama_model)
        points.append(PointStruct(id=i, vector=embeddings, payload={"text": chunk}))

    operation_info = qdrant_client.upsert(
        collection_name=collection_name,
        wait=True,
        points=points
    )
    return operation_info

def search_qdrant(query, ollama_model, collection_name, limit=3):
    embeddings = get_embedding(query, ollama_model)
    search_result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=embeddings,
        limit=limit
    )
    return search_result

