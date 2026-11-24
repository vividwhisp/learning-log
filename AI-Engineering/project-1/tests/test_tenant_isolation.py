
import json
import numpy as np

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

import src.search as search_module
import src.sparse_search as sparse_module


class FakeEmbeddingModel:
    """Avoid downloading or loading the real embedding model."""

    def __init__(self, model_name):
        pass

    def encode(self, text, convert_to_numpy=True):
        return np.array([1.0] + [0.0] * 383)


def test_cross_tenant_isolation(tmp_path, monkeypatch):
    collection = "tenant_isolation_test"
    db_path = tmp_path / "qdrant_test"
    chunks_path = tmp_path / "test_chunks.json"

    # Four synthetic documents: one shared document per tenant
    # and one unrelated document per tenant.
    chunks = [
        {
            "id": "alice-001",
            "title": "Alice Shared Notes",
            "source": "alice.md",
            "chunk_index": 0,
            "text": "This is a shared project document for Alice.",
            "tenant_id": "alice_001",
        },
        {
            "id": "alice-002",
            "title": "Alice Private Notes",
            "source": "alice.md",
            "chunk_index": 1,
            "text": "Alice has a private document about databases.",
            "tenant_id": "alice_001",
        },
        {
            "id": "bob-001",
            "title": "Bob Shared Notes",
            "source": "bob.md",
            "chunk_index": 0,
            "text": "This is a shared project document for Bob.",
            "tenant_id": "bob_001",
        },
        {
            "id": "bob-002",
            "title": "Bob Private Notes",
            "source": "bob.md",
            "chunk_index": 1,
            "text": "Bob has a private document about networking.",
            "tenant_id": "bob_001",
        },
        {
        "id": "other-001",
        "title": "Other Notes One",
        "source": "other_one.md",
        "chunk_index": 0,
        "text": "A document about machine learning algorithms.",
        "tenant_id": "other_001",
    },
    {
        "id": "other-002",
        "title": "Other Notes Two",
        "source": "other_two.md",
        "chunk_index": 0,
        "text": "A document about cloud infrastructure.",
        "tenant_id": "other_001",
    },
    ]

    chunks_path.write_text(json.dumps(chunks), encoding="utf-8")

    # Redirect the real search classes to temporary resources.
    monkeypatch.setattr(search_module, "DB_PATH", db_path)
    monkeypatch.setattr(search_module, "COLLECTION", collection)
    monkeypatch.setattr(
        search_module,
        "SentenceTransformer",
        FakeEmbeddingModel,
    )
    monkeypatch.setattr(
        sparse_module,
        "CHUNKS_FILE",
        chunks_path,
    )

    # Create a separate temporary Qdrant collection.
    client = QdrantClient(path=str(db_path))

    client.create_collection(
        collection_name=collection,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE,
        ),
    )

    points = [
        PointStruct(
            id=index,
            vector=[1.0] + [0.0] * 383,
            payload=chunk,
        )
        for index, chunk in enumerate(chunks, start=1)
    ]

    client.upsert(
        collection_name=collection,
        points=points,
    )

    client.close()

    # Test the actual retrieval classes.
    dense = search_module.SemanticSearch()
    sparse = sparse_module.BM25Search()

    try:
        for tenant_id, expected_title in [
            ("alice_001", "Alice Shared Notes"),
            ("bob_001", "Bob Shared Notes"),
        ]:
            dense_results = dense.search(
                query="shared",
                tenant_id=tenant_id,
                limit=5,
            )

            sparse_results = sparse.search(
                query="shared",
                tenant_id=tenant_id,
                limit=5,
            )

            # Each tenant must retrieve its own document.
            assert len(dense_results) == 2
            assert len(sparse_results) == 1
            assert expected_title in [
                result["title"] for result in dense_results
                ]
            assert sparse_results[0]["title"] == expected_title

            # Every returned document must belong to that tenant.
            expected_prefix = "Alice" if tenant_id == "alice_001" else "Bob"

            assert all(
                    result["title"].startswith(expected_prefix)
                    for result in dense_results
                    )

        # Unknown tenant must not retrieve anything.
        assert dense.search(
            "shared", tenant_id="mallory_001"
        ) == []

        assert sparse.search(
            "shared", tenant_id="mallory_001"
        ) == []

    finally:
        dense.close()
