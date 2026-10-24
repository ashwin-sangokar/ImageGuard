import hashlib
from pathlib import Path

def calculate_sha256(file_path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()

def compare_hashes(calculated_hash, reference_hash):
    reference_hash = reference_hash.strip().lower()
    if len(reference_hash) != 64 or any(ch not in "0123456789abcdef" for ch in reference_hash):
        raise ValueError("Reference SHA-256 must contain exactly 64 hexadecimal characters.")
    return calculated_hash.lower() == reference_hash
