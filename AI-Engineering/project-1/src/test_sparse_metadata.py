from src.sparse_search import BM25Search


def main():
    searcher = BM25Search()

    query = "Kubernetes Pods and deployments"

    try:
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

        print("Kubernetes:", [r["source"] for r in kubernetes])
        print("PostgreSQL:", [r["source"] for r in postgres])
        print("Unfiltered:", [r["source"] for r in unfiltered])
        print("Nonexistent:", nonexistent)

        assert all(r["source"] == "kubernetes.md" for r in kubernetes)
        assert all(r["source"] == "postgresql.md" for r in postgres)
        assert nonexistent == []

        print("\nAll sparse metadata tests passed!")

    finally:
        pass


if __name__ == "__main__":
    main()