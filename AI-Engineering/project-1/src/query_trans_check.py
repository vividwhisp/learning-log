from src.reranked_search import RerankedSearch

searcher = RerankedSearch()

queries = {
    "Original": "How do Kubernetes Services expose Pods?",
    "Rewritten": (
        "Kubernetes Services expose Pods mechanisms service types "
        "NodePort LoadBalancer ClusterIP"
    ),
}

try:
    for label, query in queries.items():
        print(f"\n{'=' * 15} {label} {'=' * 15}")

        results = searcher.search(
            query,
            limit=5,
            fetch_limit=20,
        )

        for rank, result in enumerate(results, start=1):
            print(
                f"{rank}. Chunk {result['chunk_index']} | "
                f"Rerank: {result['rerank_score']:.4f} | "
                f"{result['source']}"
            )
finally:
    searcher.close()