import torch
import ollama
import os

def load_vault_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as vault_file:
            return vault_file.readlines()
    else:
        return None

def generate_vault_embeddings(vault_content, ollama_model):
    vault_embeddings = []
    for content in vault_content:
        response = ollama.embeddings(model=ollama_model, prompt=content)
        vault_embeddings.append(response["embedding"])
    return torch.tensor(vault_embeddings)

def get_relevant_context(user_input, vault_embeddings, vault_content, ollama_model, top_k=3):
    print("Called: ollama_chat")
    if vault_embeddings.nelement() == 0:
        return []

    input_embedding = ollama.embeddings(model=ollama_model, prompt=user_input)["embedding"]

    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)

    top_k = min(top_k, len(cos_scores))
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context
