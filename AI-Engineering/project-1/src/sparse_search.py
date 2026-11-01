import json
import re

from rank_bm25 import BM25Okapi
from src.config import CHUNKS_FILE


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_./-]+", text.lower())


class BM25Search:

    def __init__(self):
        with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
            self.chunks = json.load(file)

        self.tokenized_chunks = [
            tokenize(chunk["text"])
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(self.tokenized_chunks)

    def search(self, query: str, limit: int = 5) -> list[dict]:
        query = query.strip()

        if not query:
            return []

        tokenized_query = tokenize(query)

        if not tokenized_query:
            return []

        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )

        results = []

        for index in ranked_indices:
            score = float(scores[index])

            if score <= 0:
                break

            chunk = self.chunks[index]

            results.append({
                "title": chunk["title"],
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
                "score": score,
            })

            if len(results) == limit:
                break

        return results