
import json
import uuid
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
        raise ValueError("chunks.json is empty or contains no chunks")

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

        # Store all points in one upsert operation.
        client.upsert(
            collection_name=COLLECTION,
            points=points,
        )

        print(f"Stored {len(points)} chunks in Qdrant")

        # Interactive semantic search
        while True:
            query = input(
                "\nEnter a search query (or 'exit'): "
            ).strip()

            if query.lower() == "exit":
                break

            if not query:
                print("Type query!")
                continue

            query_vector = model.encode(
                query,
                convert_to_numpy=True,
            ).tolist()

            results = client.query_points(
                collection_name=COLLECTION,
                query=query_vector,
                limit=5,
                with_payload=True,
            )

            print("\nTop results:")

            if not results.points:
                print("No results found.")
                continue

            for rank, point in enumerate(results.points, start=1):
                payload = point.payload or {}

                print(
                    f"\n{rank}. "
                    f"{payload.get('title', 'Untitled')}"
                )
                print(
                    f"Source: "
                    f"{payload.get('source', 'Unknown')}"
                )
                print(f"Score: {point.score:.4f}")
                print(payload.get("text", ""))

    finally:
        client.close()


if __name__ == "__main__":
    main()
