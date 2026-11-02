from src.sparse_search import BM25Search

searcher = BM25Search()

queries = [
    "What is a Kubernetes Pod?",
    "CrashLoopBackOff",
    "How does PostgreSQL handle transactions?",
    "Python dictionaries",
]

for query in queries:
    print(f"\nQuery: {query}")
    results = searcher.search(query, limit=5)
    for result in results:
        print(
            result["source"],
            result["chunk_index"],
            f"{result["score"]:.4f}",
        )
        print(result["text"][:200])
