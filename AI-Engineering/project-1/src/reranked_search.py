from src.hybrid_search import HybridSearch
from src.reranker import Reranker

class RerankedSearch:
    def __init__(self):
        self.hybrid_search = HybridSearch()
        self.reranker = Reranker()

    def search(self, query: str, limit : int = 5, fetch_limit : init = 20) -> list[dict]:
        candidates = self.hybrid_search.search(
            query,
            limit=fetch_limit,
            fetch_limit=fetch_limit,
        )

        return self.reranker.rerank(
            query,
            candidates,
            limit=limit,
        )

    def close(self):
        self.hybrid_search.close()