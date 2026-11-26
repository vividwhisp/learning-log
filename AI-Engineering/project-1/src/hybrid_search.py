from src.search import SemanticSearch
from src.sparse_search import BM25Search

class HybridSearch:
    def __init__(self, dense_search=None, sparse_search=None):
        self.dense_search = dense_search or SemanticSearch()
        self.sparse_search = sparse_search or BM25Search()

    def search(self, query: str, tenant_id: str, limit : int = 5, fetch_limit: int = 10, k : int = 60, source : str | None = None) -> list[dict]:
        if not query.strip():
            return []

        dense_results = self.dense_search.search(
            query, tenant_id=tenant_id, limit=fetch_limit, source=source
        )

        sparse_results = self.sparse_search.search(
            query, tenant_id=tenant_id, limit=fetch_limit, source=source
        )

        fused = {}

        for ranked_results in (dense_results, sparse_results):
            for rank, result in enumerate(ranked_results, start=1):
                doc_id = (
                    result["source"],
                    result["chunk_index"],
                )
                if doc_id not in fused:
                    fused[doc_id] = {
                        **result,
                        "score" : 0.0,
                    }
                fused[doc_id]["score"] += 1 / (k + rank)
        ranked = sorted(
            fused.values(),
            key=lambda result : result["score"],
            reverse=True,
        )
        return ranked[:limit]

    def close(self):
        self.dense_search.close()