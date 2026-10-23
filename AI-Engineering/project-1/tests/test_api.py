from fastapi.testclient import TestClient

from src.api import app

def test_health():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status":"ok"}

def test_search_returns_results():
    with TestClient(app) as client:
        response = client.post(
            "/search",
            json = {
                "query" : "How do Kubernetes pods work?",
                "limit" : 5,
            },
        )
    assert response.status_code == 200
    data = response.json()

    assert data["query"] == "How do Kubernetes pods work?"
    assert data["total_results"] > 0
    assert len(data["results"]) <= 5

    result = data["results"][0]

    assert result["title"]
    assert result["source"]
    assert result["text"]
    assert isinstance(result["score"], (int, float))
    
def test_search_rejects_empty_query():
    with TestClient(app) as client:
        response = client.post(
            "/search",
            json={"query": "", "limit": 5},
        )

    assert response.status_code == 422


def test_search_rejects_invalid_limit():
    with TestClient(app) as client:
        response = client.post(
            "/search",
            json={"query": "Python", "limit": 100},
        )

    assert response.status_code == 422
