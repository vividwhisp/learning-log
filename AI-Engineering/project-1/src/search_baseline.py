from sentence_transformers import SentenceTransformer
import numpy as np
import torch
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHUNKS_FILE = PROJECT_ROOT / "data" / "chunks.json"

with CHUNKS_FILE.open(encoding="utf-8") as file:
    chunks = json.load(file)

def cosine_similarity(a,b):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

texts = [chunk["text"] for chunk in chunks]

embeddings = model.encode(texts, convert_to_numpy=True)
query = "What is kubernetes"

q = model.encode(query, convert_to_numpy=True)
for i, emb in enumerate(embeddings):
    score = cosine_similarity(q, emb)
    print(f"{score:.3f} {chunks[i]['title']}")