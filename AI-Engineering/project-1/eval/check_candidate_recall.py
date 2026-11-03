import json
from pathlib import Path

from src.hybrid_search import HybridSearch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUERIES_FILE = PROJECT_ROOT / "eval" / "queries.json"

CANDIDATE_LIMIT = 10

def main():
    queries = json.loads(QUERIES_FILE.read_text(encoding="utf-8"))
    searcher = HybridSearch()

    total_relevant = 0
    found_relevant = 0

    try:
        for item in queries:
            relevant = {
                (chunk["source"], chunk["chunk_index"])
                for chunk in item["relevant_chunks"]

            }
            results = searcher.search(
                item["query"],
                limit=CANDIDATE_LIMIT,
                fetch_limit=20
            )

            retrieved = {
                (result["source"], result["chunk_index"])
                for result in results
            }

            found = relevant & retrieved

            total_relevant += len(relevant)
            found_relevant += len(found)

            print(f"\nQuery: {item["query"]}")
            print(f"Found: {len(found)/ len(relevant)}")

            missing = relevant - retrieved
            if missing:
                print(f"Missing Candidates: {sorted(missing)}")
        print(
            f"\nHybrid Candidate Recall@{CANDIDATE_LIMIT}: "
            f"{found_relevant / total_relevant:.2%}"
        )
    finally:
        searcher.close()

if __name__== "__main__":
    main()