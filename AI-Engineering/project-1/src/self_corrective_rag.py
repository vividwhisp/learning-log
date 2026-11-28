from src.reranked_search import RerankedSearch
from src.relevance_grader import grade_relevance
class SelfCorrectiveRAG:
    def __init__(self, searcher=None):
        self.searcher = searcher or RerankedSearch()

    def retrieve_and_grade(self, query, tenant_id, limit=5, source=None):
        if not query.strip():
            raise ValueError("Query cannot be empty")

        results = self.searcher.search(
            query,
            tenant_id=tenant_id,
            limit=limit,
            source=source,
        )

        grade = grade_relevance(
            question=query,
            results=results,
        )

        return {
        "results": results,
        "grade": grade,
            }