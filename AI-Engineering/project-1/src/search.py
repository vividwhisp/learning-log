from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
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

    
    def search(
        self,
        query: str,
        tenant_id: str,
        limit: int = 5,
        source: str | None = None,
    ) -> list[dict]:

        query = query.strip()
        if not query:
            return []

        if not tenant_id:
            raise ValueError("tenant_id is required")

        query_vector = self.model.encode(
            query,
            convert_to_numpy=True,
        ).tolist()

        conditions = [
            FieldCondition(
                key="tenant_id",
                match=MatchValue(value=tenant_id),
            )
        ]

        if source is not None:
            conditions.append(
                FieldCondition(
                    key="source",
                    match=MatchValue(value=source),
                )
            )

        query_filter = Filter(must=conditions)

        response = self.client.query_points(
            collection_name=COLLECTION,
            query=query_vector,
            limit=limit,
            with_payload=True,
            query_filter=query_filter,
        )

        results = []

        for point in response.points:
            payload = point.payload or {}

            results.append({
                "title": payload.get("title", "Untitled"),
                "source": payload.get("source", "Unknown"),
                "chunk_index": payload.get("chunk_index"),
                "text": payload.get("text", ""),
                "score": point.score,
            })

        return results


    def close(self):
        self.client.close()
