from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from src.config import (
    COLLECTION, DB_PATH,MODEL_NAME,
)

class SemanticSearch:
    def __init__(self):
        self.client = QdrantClient(path=str(DB_PATH))

        try:
            if not self.client.collection_exists(COLLECTION):
                raise RuntimeError(
                    "Search index not found"
                    "Run `python -m src.index first."
                )
            self.model = SentenceTransformer(MODEL_NAME)

        except Exception:
            self.client.close()
            raise

    def search(self, query:str, limit: int = 5) -> list[dict]:
        query = query.strip()
        if not query:
            return []

        query_vector = self.model.encode(
            query,
            convert_to_numpy=True,

        ).tolist()
        response = self.client.query_points(
            collection_name = COLLECTION,
            query=query_vector,
            limit=limit,
            with_payload = True,
        )
        results = []

        for point in response.points:
            payload = point.payload or {}

            results.append(
                {
                    "title": payload.get("title", "Untitled"),
                    "source": payload.get("source", "Unknown"),
                    "chunk_index": payload.get("chunk_index"),
                    "text": payload.get("text", ""),
                    "score": point.score,
                }
            )

        return results

    def close(self):
        self.client.close()
