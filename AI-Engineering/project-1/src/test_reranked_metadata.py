from src.reranked_search import RerankedSearch


def main():
    searcher = RerankedSearch()

    try:
        query = "How do Kubernetes Pods work?"

        kubernetes = searcher.search(
            query, limit=5, source="kubernetes.md"
        )

        postgres = searcher.search(
            query, limit=5, source="postgresql.md"
        )

        unfiltered = searcher.search(query, limit=5)

        nonexistent = searcher.search(
            query, limit=5, source="nonexistent.md"
        )

        for name, results in [
            ("Kubernetes", kubernetes),
            ("PostgreSQL", postgres),
            ("Unfiltered", unfiltered),
            ("Nonexistent", nonexistent),
        ]:
            print(f"\n{name}:")
            for result in results:
                print(result["source"], result["chunk_index"])

        assert all(r["source"] == "kubernetes.md" for r in kubernetes)
        assert all(r["source"] == "postgresql.md" for r in postgres)
        assert nonexistent == []

        print("\nAll reranked metadata tests passed!")

    finally:
        searcher.close()


if __name__ == "__main__":
    main()