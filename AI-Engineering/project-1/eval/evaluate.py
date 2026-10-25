import json
from pathlib import Path

from src.search import SemanticSearch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUERIES_FILE = PROJECT_ROOT / "eval" / "queries.json"

def main():
    queries = json.loads(QUERIES_FILE.read_text())
    searcher = SemanticSearch()

    try:
        hits = 0
        for item in queries:
            results = searcher.search(item['query'], limit=5)

            found = any(
                result["source"].endswith(item["expected_source"])
                for result in results
            )
            hits += int(found)

            print(f"\nQuery: {item['query']}")
            print(f"Expected source: {item['expected_source']}")
            print(f"Found in top 5: {found}")

            for rank, result in enumerate(results, start=1):
                print(
                    f"{rank}. {result['source']} "
                    f"(score={result['score']:.4f})"
                )
        print(f"\nRecall@5: {hits / len(queries):.2%}")
    finally:
        searcher.close()

if __name__ == "__main__":
    main()
        