
import json
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

from src.config import (
    CHUNKS_FILE,
    COLLECTION,
    DB_PATH,
    MODEL_NAME,
    VECTOR_SIZE,
)


def main():
    with CHUNKS_FILE.open(encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        raise ValueError("No chunks found in chunks.json")

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

    try:
        # Rebuild the collection only when explicitly indexing.
        if client.collection_exists(COLLECTION):
            client.delete_collection(COLLECTION)

        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

        points = []

        for chunk, embedding in zip(chunks, embeddings):
            points.append(
                PointStruct(
                    id=str(
                        uuid.uuid5(
                            uuid.NAMESPACE_URL,
                            chunk["id"],
                        )
                    ),
                    vector=embedding.tolist(),
                    payload={
                        "title": chunk["title"],
                        "source": chunk["source"],
                        "chunk_index": chunk["chunk_index"],
                        "text": chunk["text"],
                    },
                )
            )

        client.upsert(
            collection_name=COLLECTION,
            points=points,
        )

        print(f"Indexed {len(points)} chunks successfully.")

    finally:
        client.close()


if __name__ == "__main__":
    main()
