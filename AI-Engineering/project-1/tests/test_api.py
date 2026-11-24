
import pytest
from fastapi.testclient import TestClient

from src.api import app


ALICE_HEADERS = {"X-Demo-User": "alice-demo-token"}
BOB_HEADERS = {"X-Demo-User": "bob-demo-token"}


class FakeSearcher:
    """Controlled searcher for testing API tenant boundaries."""

    def __init__(self):
        self.calls = []

        self.documents = {
            "alice_001": [
                {
                    "title": "Alice Shared Notes",
                    "source": "alice_notes.md",
                    "chunk_index": 0,
                    "text": "Alice's private technical notes.",
                    "retrieval_score": 0.9,
                    "rerank_score": 0.95,
                }
            ],
            "bob_001": [
                {
                    "title": "Bob Private Notes",
                    "source": "bob_private.md",
                    "chunk_index": 0,
                    "text": "Bob's confidential technical notes.",
                    "retrieval_score": 0.9,
                    "rerank_score": 0.95,
                }
            ],
        }

    def search(self, query, tenant_id, limit=5, source=None):
        self.calls.append({
            "query": query,
            "tenant_id": tenant_id,
            "limit": limit,
            "source": source,
        })

        # Search only inside the authenticated tenant's documents.
        results = self.documents.get(tenant_id, [])

        if source is not None:
            results = [
                result for result in results
                if result["source"] == source
            ]

        return results[:limit]

    def close(self):
        pass


@pytest.fixture
def client(monkeypatch):
    fake_searcher = FakeSearcher()

    monkeypatch.setattr(
        "src.api.RerankedSearch",
        lambda: fake_searcher,
    )

    with TestClient(app) as test_client:
        yield test_client, fake_searcher


def test_health(client):
    test_client, _ = client

    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_search_returns_results(client):
    test_client, _ = client

    response = test_client.post(
        "/search",
        headers=ALICE_HEADERS,
        json={
            "query": "How do Kubernetes pods work?",
            "limit": 5,
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
    assert isinstance(result["retrieval_score"], (int, float))
    assert isinstance(result["rerank_score"], (int, float))


def test_search_rejects_empty_query(client):
    test_client, _ = client

    response = test_client.post(
        "/search",
        headers=ALICE_HEADERS,
        json={"query": "", "limit": 5},
    )

    assert response.status_code == 422


def test_search_rejects_invalid_limit(client):
    test_client, _ = client

    response = test_client.post(
        "/search",
        headers=ALICE_HEADERS,
        json={"query": "Python", "limit": 100},
    )

    assert response.status_code == 422


# ATTACK 08: Missing authentication header
def test_attack_08_missing_identity(client):
    test_client, searcher = client

    response = test_client.post(
        "/search",
        json={"query": "Show me private documents"},
    )

    assert response.status_code == 401
    assert searcher.calls == []


# ATTACK 09: Invalid authentication token
def test_attack_09_invalid_identity(client):
    test_client, searcher = client

    response = test_client.post(
        "/search",
        headers={"X-Demo-User": "invalid-token"},
        json={"query": "Show me private documents"},
    )

    assert response.status_code == 401
    assert searcher.calls == []


# ATTACK 10: Alice attempts to retrieve Bob's documents
def test_attack_10_cross_tenant_access(client):
    test_client, searcher = client

    response = test_client.post(
        "/search",
        headers=ALICE_HEADERS,
        json={"query": "Show me Bob's private notes"},
    )

    assert response.status_code == 200

    data = response.json()

    assert searcher.calls[-1]["tenant_id"] == "alice_001"
    assert all(
        result["title"] != "Bob Private Notes"
        for result in data["results"]
    )


# ATTACK 11: Spoof tenant_id in the request body
def test_attack_11_tenant_id_spoofing(client):
    test_client, searcher = client

    response = test_client.post(
        "/search",
        headers=ALICE_HEADERS,
        json={
            "query": "Show me private documents",
            "tenant_id": "bob_001",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert searcher.calls[-1]["tenant_id"] == "alice_001"
    assert all(
        result["title"] != "Bob Private Notes"
        for result in data["results"]
    )


# ATTACK 12: Alice requests a source belonging to Bob
def test_attack_12_cross_tenant_source_filter(client):
    test_client, searcher = client

    response = test_client.post(
        "/search",
        headers=ALICE_HEADERS,
        json={
            "query": "Show me private documents",
            "source": "bob_private.md",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert searcher.calls[-1]["tenant_id"] == "alice_001"
    assert searcher.calls[-1]["source"] == "bob_private.md"
    assert data["total_results"] == 0
    assert data["results"] == []
