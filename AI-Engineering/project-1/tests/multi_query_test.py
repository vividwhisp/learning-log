
from src.multi_query_search import MultiQuerySearch


def main():
    searcher = MultiQuerySearch()

    query = "How do Kubernetes Services expose Pods?"

    try:
        print(f"\nOriginal query: {query}")

        results = searcher.search(
            query=query,
            limit=5,
            fetch_limit=20,
            num_queries=3,
        )

        print("\n========== MULTI-QUERY RESULTS ==========")

        if not results:
            print("No results found.")
            return

        for rank, result in enumerate(results, start=1):
            source = result["source"]
            chunk_index = result["chunk_index"]
            title = result["title"]
            retrieval_score = result["retrieval_score"]
            rerank_score = result["rerank_score"]

            print(f"\nRank: {rank}")
            print(f"Title: {title}")
            print(f"Source: {source}")
            print(f"Chunk: {chunk_index}")
            print(f"RRF Score: {retrieval_score:.6f}")
            print(f"Rerank Score: {rerank_score:.4f}")
            print(f"Text: {result['text'][:300]}...")

    finally:
        searcher.close()


if __name__ == "__main__":
    main()
