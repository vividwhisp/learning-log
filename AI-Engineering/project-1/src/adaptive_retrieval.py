import re
from src.search import SemanticSearch
from src.sparse_search import BM25Search
from src.hybrid_search import HybridSearch
from src.reranked_search import RerankedSearch
def classify_query(query: str) -> str:
    query = query.strip().lower()

    if not query:
        raise ValueError("Query Cannot be empty")

    troubleshooting_terms={
        "troubleshoot",
        "debug",
        "fix",
        "resolve",
        "why is",
        "why does",
        "not working",
        "failing",
        "error",
        "issue",
        "problem",
    }

    if(
        sum(term in query for term in troubleshooting_terms) >= 2
        or any(term in query for term in {
            "how do i fix",
            "how do i troubleshoot",
            "step by step",
        })
    ):
        return "reranked"

    identifier_patterns = [
        r"\b[A-Z][a-zA-Z0-9]*BackOff\b",
        r"\b[A-Z][a-zA-Z0-9]*Error\b",
        r"\b[A-Z][a-zA-Z0-9]*Failed\b",
        r"\bHTTP\s*\d{3}\b",
        r"\b\d{3,5}\b",
    ]   

    if any(re.search(pattern, query, re.IGNORECASE) for pattern in identifier_patterns):
        return "sparse"

    technical_terms = {
        "kubernetes", "deployment", "pod", "replicaset",
        "container", "api", "docker", "qdrant",
        "fastapi", "configmap", "secret", "service",
    }

    words = set(re.findall(r"\b\w+\b", query))
    technical_matches = words.intersection(technical_terms)

    if len(technical_matches) >= 2 or (
        technical_matches and len(words) >= 8
    ):
        return "hybrid"

    return "dense"
class AdaptiveRetriever:

    def __init__(self):
        self.dense = SemanticSearch()
        self.sparse = BM25Search()

        self.hybrid = HybridSearch(
            dense_search=self.dense,
            sparse_search=self.sparse,
        )

        self.reranked = RerankedSearch(
            hybrid_search=self.hybrid,
        )

    def search(
        self,
        query: str,
        tenant_id: str,
        limit: int = 5,
        source: str | None = None,
    ) -> dict:

        strategy = classify_query(query)

        if strategy == "dense":
            results = self.dense.search(
                query, tenant_id, limit, source
            )

        elif strategy == "sparse":
            results = self.sparse.search(
                query, tenant_id, limit, source
            )

        elif strategy == "hybrid":
            results = self.hybrid.search(
                query, tenant_id, limit, source=source
            )

        else:
            results = self.reranked.search(
                query, tenant_id, limit, source=source
            )

        return {
            "query": query,
            "strategy": strategy,
            "results": results,
        }

    def close(self):
        self.dense.close()