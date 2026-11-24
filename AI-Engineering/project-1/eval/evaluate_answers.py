import json
from pathlib import Path

from src.reranked_search import RerankedSearch
from src.generation import generate_rag_answer
from src.citations import extract_citations

ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "eval" /"answer_queries.json"
OUTPUT_PATH = ROOT / "eval" / "answer_results.json"

def main():
    with open(DATASET_PATH, encoding="utf-8") as file:
        test_cases = json.load(file)

    searcher = RerankedSearch()
    evaluation_results = []

    try:
        for case in test_cases:
            question = case["question"]

            print(f"\nEvaluating {case['id']} : {question}")
            results = searcher.search(
                query=question,
                tenant_id="alice_001",
                limit=5,
            )

            answer = generate_rag_answer(question, results)
            citations = extract_citations(answer, results)

            evaluation_results.append({
                **case,
                "generated_answer": answer,
                "retrieved_results": results,
                "extracted_citations":citations,
            }
            )
            print("Answer: ",answer)
            print("Citations: ",citations)
    finally:
        searcher.close()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(evaluation_results, file, indent=2,ensure_ascii=False)

    print(f"\nEvaluation complete. Results saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()