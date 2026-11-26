from src.adaptive_retrieval import classify_query

test_queries = [
    "What is container orchestration?",
    "ImagePullBackOff",
    "How does Kubernetes deployment manage replicas?",
    "Why is my Kubernetes deployment failing and how do I fix it?",
]

for query in test_queries:
    strategy = classify_query(query)
    print(f"Query: {query}")
    print(f"Strategy: {strategy}\n")
