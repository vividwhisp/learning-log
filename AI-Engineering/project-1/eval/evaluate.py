import time
import json
from pathlib import Path
from collections import Counter
from src.hybrid_search import HybridSearch
from src.reranker import Reranker
from src.adaptive_retrieval import AdaptiveRetriever

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUERIES_FILE = PROJECT_ROOT / "eval" / "queries.json"

LIMIT = 5


def chunk_id(result):
    return (result["source"], result["chunk_index"])


def evaluate_retriever(name, search_function, queries, debug_candidates=None,):
    total_relevant = 0
    retrieved_relevant = 0
    reciprocal_ranks = []
    successful_queries = 0
    latencies = []
    

    print(f"\n{'=' * 65}")
    print(f"Evaluating: {name}")
    print("=" * 65)

    for item in queries:
        query = item["query"]

        relevant = {
            (chunk["source"], chunk["chunk_index"])
            for chunk in item["relevant_chunks"]
        }

        start = time.perf_counter()
        results = search_function(query, tenant_id="alice_001", limit=LIMIT)
        latencies.append((time.perf_counter() - start) * 1000)
        retrieved = [chunk_id(result) for result in results]

        relevant_ranks = [
            rank
            for rank, result in enumerate(results, start=1)
            if chunk_id(result) in relevant
        ]

        found_relevant = len(set(retrieved) & relevant)
        missing = relevant - set(retrieved)
        if debug_candidates is not None:
            data = debug_candidates[query]

            for chunk in missing:
               candidate_rank = next(
                   (
                       rank
                       for rank, result in enumerate(
                           data["candidates"], start = 1
                       )
                       if chunk_id(result) == chunk
                   ),
                   None,
                ) 
               if candidate_rank is None:
                    print(f"ABSENT FROM CANDIDATES: {chunk}")
               else:
                    print(
                        f"RERANKED BELOW TOP 5: {chunk} "
                        f"(hybrid candidate rank: {candidate_rank})"
                        )

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
            score = result.get("rerank_score", result["score"])

            print(
                f"{marker} {rank}. {result['source']} "
                f"(chunk={result['chunk_index']}, "
                f"score={score:.4f})"
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
        "avg_latency_ms": sum(latencies) / len(latencies) if latencies else 0,
    }

def main():
    queries = json.loads(QUERIES_FILE.read_text(encoding="utf-8"))

    if not queries:
        raise ValueError("Evaluation dataset is empty.")

    results = []

    hybrid_results_by_query = {}
    adaptive_results_by_query = {}
    strategy_by_query = {}
    strategy_counts = {}

    # 1. Baseline: Hybrid RRF
    searcher = HybridSearch()
    try:
        def hybrid_search(query, tenant_id, limit=5):
            retrieved = searcher.search(
                query,
                tenant_id=tenant_id,
                limit=limit,
            )
            hybrid_results_by_query[query] = retrieved
            return retrieved

        results.append(
            evaluate_retriever(
                "Hybrid Retrieval (RRF)",
                hybrid_search,
                queries,
            )
        )
    finally:
        searcher.close()

    # 2. Adaptive retrieval
    # The baseline Qdrant client is closed before this is initialized.
    adaptive = AdaptiveRetriever()
    try:
        def adaptive_search(query, tenant_id, limit=5):
            response = adaptive.search(
                query,
                tenant_id=tenant_id,
                limit=limit,
            )

            strategy = response["strategy"]
            retrieved = response["results"]

            strategy_by_query[query] = strategy
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
            adaptive_results_by_query[query] = retrieved

            return retrieved

        results.append(
            evaluate_retriever(
                "Adaptive Retrieval",
                adaptive_search,
                queries,
            )
        )
    finally:
        adaptive.close()

    # 3. Overall metric comparison
    print("\n" + "=" * 75)
    print("FINAL COMPARISON")
    print("=" * 75)

    print(
        f"{'Retriever':<28}"
        f"{'Recall@5':<12}"
        f"{'MRR@5':<12}"
        f"{'HitRate@5':<12}"
        f"{'Avg latency':<14}"
    )

    for result in results:
        print(
            f"{result['name']:<28}"
            f"{result['recall']:<12.2%}"
            f"{result['mrr']:<12.4f}"
            f"{result['hit_rate']:<12.2%}"
            f"{result['avg_latency_ms']:.2f} ms"
        )

    # 4. Count how often each adaptive strategy was selected
    print("\nSTRATEGY COUNTS")
    for strategy, count in sorted(strategy_counts.items()):
        print(f"{strategy}: {count}")

    # 5. Compare the first relevant result's rank for each query
    def first_relevant_rank(retrieved, relevant_chunks):
        relevant_ids = {
            (chunk["source"], chunk["chunk_index"])
            for chunk in relevant_chunks
        }

        for rank, result in enumerate(retrieved, start=1):
            if chunk_id(result) in relevant_ids:
                return rank

        return None

    print("\nPER-QUERY RANKING COMPARISON")
    for item in queries:
        query = item["query"]
        relevant = item["relevant_chunks"]

        hybrid_rank = first_relevant_rank(
            hybrid_results_by_query[query],
            relevant,
        )
        adaptive_rank = first_relevant_rank(
            adaptive_results_by_query[query],
            relevant,
        )

        print(f"\nQuery: {query}")
        print(f"Strategy: {strategy_by_query[query]}")
        print(f"Hybrid first relevant rank: {hybrid_rank}")
        print(f"Adaptive first relevant rank: {adaptive_rank}")


if __name__ == "__main__":
    main()