from src.hybrid_search import HybridSearch
from src.reranker import Reranker

class RerankedSearch:
    def __init__(self):
        self.hybrid_search = HybridSearch()
        self.reranker = Reranker()

    def search(self, query: str, limit : int = 5, fetch_limit : int = 20, source : str | None = None) -> list[dict]:
        candidates = self.hybrid_search.search(
            query,
            limit=fetch_limit,
            fetch_limit=fetch_limit,
            source=source,
        )

        return self.reranker.rerank(
            query,
            candidates,
            limit=limit,
        )

    def close(self):
        self.hybrid_search.close()