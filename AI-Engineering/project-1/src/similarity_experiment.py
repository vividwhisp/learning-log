from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
# Two lists of sentences
sentences1 = [
    "The new movie is awesome",
    "The cat sits outside",
    "A man is playing guitar",
]

sentences2 = [
    "The new movie is awesome",
    "The dog plays in the garden",
    "A woman watches TV",
]

# Compute embeddings for both lists
embeddings1 = model.encode(sentences1)
embeddings2 = model.encode(sentences2)

# Compute cosine similarities
for i in range(len(sentences1)):
    score = cosine_similarity(
        embeddings1[i],
        embeddings2[i]
    )

    print(f"\n {sentences1[i]}")
    print(f"{sentences2[i]}")
    print(f"Similarity: {score:.4f}")

