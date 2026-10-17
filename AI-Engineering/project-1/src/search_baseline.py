from sentence_transformers import SentenceTransformer
import numpy as np
import torch


def cosine_similarity(a,b):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

documents = [
    {
        "title": "Kubernetes Pods",
        "text": "A Pod is the smallest deployable unit in Kubernetes. "
                "It contains one or more containers."
    },
    {
        "title": "Container Restart Policies",
        "text": "Kubernetes uses restart policies to determine "
                "whether containers should restart after termination."
    },
    {
        "title": "PostgreSQL Transactions",
        "text": "Transactions group database operations into a single "
                "logical unit of work."
    },
    {
        "title": "Python Functions",
        "text": "Functions are reusable blocks of code that can accept "
                "arguments and return values."
    },
    {
        "title": "Docker Images",
        "text": "A Docker image is a template used to create containers."
    },
    {
        "title": "Kubernetes Services",
        "text": "A Kubernetes Service provides a stable network endpoint "
                "for accessing a group of Pods."
    },
    {
        "title": "Database Indexes",
        "text": "Indexes help databases find records efficiently "
                "without scanning every row."
    },
    {
        "title": "Python Exceptions",
        "text": "Exceptions represent errors that occur during program "
                "execution and can be handled using try and except."
    },
]
texts = [f"{d["title"]} . {d["text"]}" for d in documents]

embeddings = model.encode(texts, convert_to_numpy=True)
print(embeddings.shape)

query = "What is a volcano?"
q = model.encode(query, convert_to_numpy=True)
for i, emb in enumerate(embeddings):
    score = cosine_similarity(q, emb)
    print(f"{score:.3f} {documents[i]['title']}")