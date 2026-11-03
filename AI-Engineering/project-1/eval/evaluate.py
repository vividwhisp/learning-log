
import json
from pathlib import Path

from src.hybrid_search import HybridSearch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUERIES_FILE = PROJECT_ROOT / "eval" / "queries.json"

LIMIT = 5


def chunk_id(result):
    return (result["source"], result["chunk_index"])


def evaluate_retriever(name, search_function, queries):
    total_relevant = 0
    retrieved_relevant = 0
    reciprocal_ranks = []
    successful_queries = 0

    print(f"\n{'=' * 65}")
    print(f"Evaluating: {name}")
    print("=" * 65)

    for item in queries:
        query = item["query"]

        relevant = {
            (chunk["source"], chunk["chunk_index"])
            for chunk in item["relevant_chunks"]
        }

        results = search_function(query, limit=LIMIT)
        retrieved = [chunk_id(result) for result in results]

        relevant_ranks = [
            rank
            for rank, result in enumerate(results, start=1)
            if chunk_id(result) in relevant
        ]

        found_relevant = len(set(retrieved) & relevant)

        total_relevant += len(relevant)
        retrieved_relevant += found_relevant

        if relevant_ranks:
            successful_queries += 1
            reciprocal_ranks.append(1 / relevant_ranks[0])
        else:
            reciprocal_ranks.append(0)

        print(f"\nQuery: {query}")
        print(f"Relevant chunks: {sorted(relevant)}")
        print(f"Relevant chunks found: {found_relevant}/{len(relevant)}")

        for rank, result in enumerate(results, start=1):
            marker = "*" if chunk_id(result) in relevant else " "
            print(
                f"{marker} {rank}. {result['source']} "
                f"(chunk={result['chunk_index']}, "
                f"score={result['score']:.4f})"
            )

    recall = (
        retrieved_relevant / total_relevant
        if total_relevant else 0
    )
    mrr = sum(reciprocal_ranks) / len(queries) if queries else 0
    hit_rate = successful_queries / len(queries) if queries else 0

    return {
        "name": name,
        "recall": recall,
        "mrr": mrr,
        "hit_rate": hit_rate,
    }


def main():
    queries = json.loads(QUERIES_FILE.read_text(encoding="utf-8"))

    if not queries:
        raise ValueError("Evaluation dataset is empty.")

    searcher = HybridSearch()

    try:
        results = [
            evaluate_retriever(
                "Dense Retrieval",
                searcher.dense_search.search,
                queries,
            ),
            evaluate_retriever(
                "Sparse Retrieval (BM25)",
                searcher.sparse_search.search,
                queries,
            ),
            evaluate_retriever(
                "Hybrid Retrieval (RRF)",
                searcher.search,
                queries,
            ),
        ]

        print("\n" + "=" * 65)
        print("FINAL COMPARISON")
        print("=" * 65)

        print(
            f"{'Retriever':<28}"
            f"{'Recall@5':<12}"
            f"{'MRR@5':<12}"
            f"{'HitRate@5'}"
        )

        for result in results:
            print(
                f"{result['name']:<28}"
                f"{result['recall']:<12.2%}"
                f"{result['mrr']:<12.4f}"
                f"{result['hit_rate']:.2%}"
            )

    finally:
        searcher.close()


if __name__ == "__main__":
    main()
