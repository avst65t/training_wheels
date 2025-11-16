import shutil
import os
import hashlib

def save_upload_file(uploaded_file, destination: str) -> str:
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return destination

def calculate_file_hash(file_path: str) -> str:
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()
