
import json
from pathlib import Path

from src.reranked_search import RerankedSearch
from src.multi_query_search import MultiQuerySearch


DATASET_PATH = Path(__file__).with_name("queries.json")


def chunk_id(result):
    return result["source"], result["chunk_index"]


def evaluate(name, queries, searcher):
    total_relevant = 0
    retrieved_relevant = 0
    reciprocal_rank_sum = 0
    successful_queries = 0

    for item in queries:
        query = item["query"]

        relevant = {
            (chunk["source"], chunk["chunk_index"])
            for chunk in item["relevant_chunks"]
        }

        results = searcher.search(
            query,
            limit=5,
            fetch_limit=20,
        )

        retrieved = [chunk_id(result) for result in results]
        found = relevant.intersection(retrieved)

        total_relevant += len(relevant)
        retrieved_relevant += len(found)

        if found:
            successful_queries += 1

            first_relevant_rank = next(
                rank
                for rank, chunk in enumerate(retrieved, start=1)
                if chunk in relevant
            )

            reciprocal_rank_sum += 1 / first_relevant_rank

        missing = relevant - set(retrieved)

        print(f"\nQuery: {query}")
        print(f"Relevant retrieved: {len(found)}/{len(relevant)}")

        if missing:
            print(f"Missing: {sorted(missing)}")

    count = len(queries)

    metrics = {
        "Recall@5": retrieved_relevant / total_relevant,
        "MRR@5": reciprocal_rank_sum / count,
        "HitRate@5": successful_queries / count,
    }

    print(f"\n========== {name} ==========")

    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

    return metrics


def main():
    with open(DATASET_PATH, encoding="utf-8") as file:
        queries = json.load(file)

    baseline_searcher = RerankedSearch()

    try:
        baseline = evaluate(
            "Baseline: Hybrid + Cross-Encoder",
            queries,
            baseline_searcher,
        )
    finally:
        baseline_searcher.close()

    multi_searcher = MultiQuerySearch()

    try:
        multi_query = evaluate(
            "Multi-Query + Hybrid + Cross-Encoder",
            queries,
            multi_searcher,
        )
    finally:
        multi_searcher.close()

    print("\n========== FINAL COMPARISON ==========")

    for metric in baseline:
        difference = multi_query[metric] - baseline[metric]

        print(
            f"{metric}: "
            f"{baseline[metric]:.4f} -> "
            f"{multi_query[metric]:.4f} "
            f"({difference:+.4f})"
        )


if __name__ == "__main__":
    main()
