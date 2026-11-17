from src.search import SemanticSearch


def main():
    searcher = SemanticSearch()

    try:
        query = "What is a Kubernetes Pod?"

        # Test 1: Filter by Kubernetes
        kubernetes = searcher.search(
            query,
            limit=5,
            source="kubernetes.md",
        )

        # Test 2: Filter by PostgreSQL
        postgres = searcher.search(
            query,
            limit=5,
            source="postgresql.md",
        )

        # Test 3: No filter
        unfiltered = searcher.search(query, limit=5)

        # Test 4: Nonexistent source
        nonexistent = searcher.search(
            query,
            limit=5,
            source="nonexistent.md",
        )

        print("\n--- Kubernetes filter ---")
        print([result["source"] for result in kubernetes])

        print("\n--- PostgreSQL filter ---")
        print([result["source"] for result in postgres])

        print("\n--- No filter ---")
        print([result["source"] for result in unfiltered])

        print("\n--- Nonexistent source ---")
        print(nonexistent)

        assert all(
            result["source"] == "kubernetes.md"
            for result in kubernetes
        )

        assert all(
            result["source"] == "postgresql.md"
            for result in postgres
        )

        assert nonexistent == []

        print("\nAll metadata filtering tests passed!")

    finally:
        searcher.close()


if __name__ == "__main__":
    main()