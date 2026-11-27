import json
from pathlib import Path

from src.relevance_grader import grade_relevance
from src.reranked_search import RerankedSearch

DATASET_PATH = Path("eval/relevance_queries.json")
TENANT_ID = "alice_001"
LIMIT = 5

def main():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        queries = json.load(file)

    searcher = RerankedSearch()
    correct = 0
    total = len(queries)

    try:
        for item in queries:
            question = item["question"]

            results = searcher.search(
                query=question,
                tenant_id=TENANT_ID,
                limit=LIMIT,
            )

            grade = grade_relevance(question, results)

            expected = item["expected_relevant"]
            predicted = grade["relevant"]

            passed = expected == predicted

            if passed:
                correct += 1

            print(f"\nQuery {item['id']}: {question}")
            print(f"Expected: {item['expected_label']}")
            print(f"Predicted: {predicted}")
            print(f"Score: {grade['score']:.2f}")
            print(f"Reason: {grade['reason']}")
            print(f"Result: {'PASS' if passed else 'FAIL'}")

    finally:
        searcher.close()
    accuracy = correct / total * 100 if total else 0

    print("\n========= EVALUATION SUMMARY =========")
    print(f"Total queries: {total}")
    print(f"Correct judgments: {correct}")
    print(f"Incorrect Judgments: {total - correct}")
    print(f"Accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()