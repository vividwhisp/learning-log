
from src.hybrid_search import HybridSearch
from src.multi_query import generate_queries
from src.reranker import Reranker


class MultiQuerySearch:
    def __init__(self):
        self.hybrid_search = HybridSearch()
        self.reranker = Reranker()

    def search(
        self,
        query: str,
        limit: int = 5,
        fetch_limit: int = 20,
        num_queries: int = 3,
        rrf_k: int = 60,
    ) -> list[dict]:

        if not query.strip():
            return []

        # Generate alternative queries.
        alternative_queries = generate_queries(
            query,
            num_queries=num_queries,
        )

        # Always retain the original query.
        queries = [query, *alternative_queries]

        fused = {}

        # Retrieve documents for every query.
        for search_query in queries:
            results = self.hybrid_search.search(
                search_query,
                limit=fetch_limit,
                fetch_limit=fetch_limit,
            )

            # Apply Reciprocal Rank Fusion across query results.
            for rank, result in enumerate(results, start=1):
                doc_id = (result["source"], result["chunk_index"])

                if doc_id not in fused:
                    fused[doc_id] = {
                        **result,
                        "score": 0.0,
                    }

                fused[doc_id]["score"] += 1 / (rrf_k + rank)

        # Rank the combined candidate pool.
        candidates = sorted(
            fused.values(),
            key=lambda result: result["score"],
            reverse=True,
        )

        # Rerank using the original user query.
        return self.reranker.rerank(
            query,
            candidates,
            limit=limit,
        )

    def close(self):
        self.hybrid_search.close()
