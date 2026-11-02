
import json
from pathlib import Path

from src.hybrid_search import HybridSearch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUERIES_FILE = PROJECT_ROOT / "eval" / "queries.json"

LIMIT = 5


def evaluate_retriever(name, search_function, queries):
    hits = 0
    reciprocal_ranks = []

    print(f"\n{'=' * 55}")
    print(f"Evaluating: {name}")
    print("=" * 55)

    for item in queries:
        query = item["query"]
        expected_source = item["expected_source"]

        results = search_function(query, limit=LIMIT)

        relevant_ranks = [
            rank
            for rank, result in enumerate(results, start=1)
            if result["source"].endswith(expected_source)
        ]

        found = bool(relevant_ranks)
        hits += int(found)

        reciprocal_rank = (
            1 / relevant_ranks[0] if found else 0
        )
        reciprocal_ranks.append(reciprocal_rank)

        print(f"\nQuery: {query}")
        print(f"Expected: {expected_source}")
        print(f"Found in top {LIMIT}: {found}")
        print(f"Reciprocal rank: {reciprocal_rank:.4f}")

        for rank, result in enumerate(results, start=1):
            print(
                f"{rank}. {result['source']} "
                f"(chunk={result['chunk_index']}, "
                f"score={result['score']:.4f})"
            )

    recall = hits / len(queries)
    mrr = sum(reciprocal_ranks) / len(queries)

    return {
        "name": name,
        "recall": recall,
        "mrr": mrr,
    }


def main():
    queries = json.loads(QUERIES_FILE.read_text())

    searcher = HybridSearch()

    try:
        results = []

        results.append(
            evaluate_retriever(
                "Dense Retrieval",
                searcher.dense_search.search,
                queries,
            )
        )

        results.append(
            evaluate_retriever(
                "Sparse Retrieval (BM25)",
                searcher.sparse_search.search,
                queries,
            )
        )

        results.append(
            evaluate_retriever(
                "Hybrid Retrieval (RRF)",
                searcher.search,
                queries,
            )
        )

        print("\n" + "=" * 55)
        print("FINAL COMPARISON")
        print("=" * 55)

        print(f"{'Retriever':<28} {'Recall@5':<12} {'MRR@5'}")

        for result in results:
            print(
                f"{result['name']:<28} "
                f"{result['recall']:<12.2%} "
                f"{result['mrr']:.4f}"
            )

    finally:
        searcher.close()


if __name__ == "__main__":
    main()
