import json
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHUNKS_FILE = PROJECT_ROOT / "data" / "chunks.json"
DB_PATH = PROJECT_ROOT / "data" / "qdrant_project1"
COLLECTION = "technical_knowledge"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_SIZE = 384

def main():
    with CHUNKS_FILE.open(encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        raise ValueError("chunks.json not found")

    model = SentenceTransformer(MODEL_NAME)
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
    )
    print(f"Chunks: {len(chunks)}")
    print(f"Embedding shape: {embeddings.shape}")

    client = QdrantClient(path=str(DB_PATH))
    