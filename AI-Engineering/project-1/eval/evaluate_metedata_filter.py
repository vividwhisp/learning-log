import json
from pathlib import Path

from src.reranked_search import RerankedSearch

DATASET_PATH = Path(__file__).with_name("queries.json")

def evaluate(name, queries, searcher, use_filter=False):
    total_relevant = 0
    retrieved_relevant = 0
    reciprocal_rank_sum = 0
    successful_queries = 0

    for item in queries:
        query = item["query"]

        relevant = {
            (chunk["source"] , chunk["chunk_index"])
            for chunk in item["relevant_chunks"]
        }

        sources = {source for source, _ in relevant}
        if len(sources) != 1:
            raise ValueError(f"Expected one source for: {query}")

        source = next(iter(sources))if use_filter else None

        results = searcher.search(
            query,
            limit=5,
            fetch_limit=20,
            source=source,
        )

        retrieved = [
            (result["source"], result["chunk_index"])
            for result in results
        ]

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

    searcher = RerankedSearch()

    try:
        baseline = evaluate(
            "Baseline: No Metadata Filter",
            queries,
            searcher,
        )

        filtered = evaluate(
            "Metadata Filter Enabled",
            queries,
            searcher,
            use_filter=True,
        )

        print("\n========== COMPARISON ==========")
        for metric in baseline:
            difference = filtered[metric] - baseline[metric]
            print(
                f"{metric}: {baseline[metric]:.4f} -> "
                f"{filtered[metric]:.4f} ({difference:+.4f})"
            )

    finally:
        searcher.close()


if __name__ == "__main__":
    main()
