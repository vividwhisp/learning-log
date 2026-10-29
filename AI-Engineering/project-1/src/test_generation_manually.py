from src.generation import generate_answer

sample_results = [
    {
        "source": "kubernetes.md",
        "chunk_index": 0,
        "text": (
            "A Pod is the smallest deployable unit in Kubernetes. "
            "It can contain one or more containers that share resources."
        ),
        "title": "Kubernetes basics",
        "score": 0.82,
    }
]

answer = generate_answer(
    "What is a Kubernetes Pod?",
    sample_results,
)

print(answer)