
import os

def load_vault_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as vault_file:
            return vault_file.readlines()
    else:
        return None



