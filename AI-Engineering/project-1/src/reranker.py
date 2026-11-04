from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self):
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
            self, 
            query : str,
            candidates : list[dict],
            limit : int = 5,
    ) -> list[dict] :
        if not query.strip() or not candidates:
            return []

        pairs = [
            (query, candidate["text"])
            for candidate in candidates
        ]

        scores = self.model.predict(pairs)

        reranked = []

        for candidate, score in zip(candidates, scores):
            result = candidate.copy()
            result["retrieval_score"] = candidate["score"]
            result["rerank_score"] = float(score)
            reranked.append(result)

        reranked.sort(
            key=lambda result: result["rerank_score"],
            reverse=True,
        )

        return reranked[:limit]