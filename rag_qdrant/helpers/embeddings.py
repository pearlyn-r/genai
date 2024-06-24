

import os
import json
import re
import pandas as pd
from helpers.qdrant_client import upsert_to_qdrant, recreate_collection

def load_vault_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as vault_file:
            return vault_file.read()
    else:
        return None

def generate_vault_embeddings(file_path, ollama_model, collection_name):
    vault_content = load_vault_content(file_path)
    if vault_content:
        print("Vault Content Loaded")
        recreate_collection(collection_name)
        operation_info = upsert_to_qdrant(vault_content, ollama_model, collection_name)
        print("Upsert Operation Info:", operation_info)
    else:
        print("File not found or is empty.")
