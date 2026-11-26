from src.adaptive_retrieval import AdaptiveRetriever

retriever = AdaptiveRetriever()

try:
    response = retriever.search(
        query="Why is my Kubernetes deployment failing and how do I troubleshoot the error?",
        tenant_id="alice_001",
        limit=5,
    )

    print("Strategy:", response["strategy"])
    print("Results:", len(response["results"]))

finally:
    retriever.close()