
import json
from pathlib import Path

from src.hybrid_search import HybridSearch
from src.reranker import Reranker


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
    }


def main():
    queries = json.loads(QUERIES_FILE.read_text(encoding="utf-8"))

    if not queries:
        raise ValueError("Evaluation dataset is empty.")

    searcher = HybridSearch()
    reranker = Reranker()
    debug_candidates = {}

    try:
        def hybrid_reranked_search(query, limit=5):
            candidates = searcher.search(
                query,
                limit=20,
                fetch_limit=20,
            )

            reranked = reranker.rerank(
                query,
                candidates,
                limit=limit,
            )
            debug_candidates[query] = {
                "candidates" : candidates,
                "reranked" : reranked,
            }
            return reranked
        

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
            evaluate_retriever(
                "Hybrid + Cross-Encoder",
                hybrid_reranked_search,
                queries,
                debug_candidates=debug_candidates,
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
