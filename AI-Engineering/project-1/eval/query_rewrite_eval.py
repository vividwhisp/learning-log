import json
from pathlib import Path

from src.query_transform import rewrite_query
from src.reranked_search import RerankedSearch


DATASET_PATH = Path(__file__).with_name("queries.json")


def chunk_id(result):
    return (result["source"], result["chunk_index"])


def evaluate(name, queries, searcher, rewrites=None):
    total_relevant = 0
    retrieved_relevant = 0
    reciprocal_rank_sum = 0
    successful_queries = 0

    for item in queries:
        original_query = item["query"]

        search_query = (
            rewrites[original_query]
            if rewrites is not None
            else original_query
        )

        results = searcher.search(
            search_query,
            limit=5,
            fetch_limit=20,
        )

        relevant = {
            (chunk["source"], chunk["chunk_index"])
            for chunk in item["relevant_chunks"]
        }

        retrieved = [chunk_id(result) for result in results]

        total_relevant += len(relevant)
        found = relevant.intersection(retrieved)
        retrieved_relevant += len(found)

        if found:
            successful_queries += 1

            first_relevant_rank = next(
                rank
                for rank, chunk in enumerate(retrieved, start=1)
                if chunk in relevant
            )

            reciprocal_rank_sum += 1 / first_relevant_rank

    count = len(queries)

    metrics = {
        "Recall@5": retrieved_relevant / total_relevant,
        "MRR@5": reciprocal_rank_sum / count,
        "HitRate@5": successful_queries / count,
    }

    print(f"\n{'=' * 15} {name} {'=' * 15}")

    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

    return metrics


def main():
    with open(DATASET_PATH, encoding="utf-8") as file:
        queries = json.load(file)

    # Generate each rewrite only once.
    rewrites = {}

    print("Generating rewritten queries...")

    for item in queries:
        original = item["query"]
        rewrites[original] = rewrite_query(original)

        print(f"\nOriginal:  {original}")
        print(f"Rewritten: {rewrites[original]}")

    searcher = RerankedSearch()

    try:
        baseline = evaluate(
            "Original Queries",
            queries,
            searcher,
        )

        transformed = evaluate(
            "Rewritten Queries",
            queries,
            searcher,
            rewrites,
        )

        print("\n========== COMPARISON ==========")

        for metric in baseline:
            difference = transformed[metric] - baseline[metric]
            print(
                f"{metric}: "
                f"{baseline[metric]:.4f} -> "
                f"{transformed[metric]:.4f} "
                f"({difference:+.4f})"
            )

    finally:
        searcher.close()


if __name__ == "__main__":
    main()
