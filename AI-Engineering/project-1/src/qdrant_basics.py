from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance ,PointStruct, VectorParams

COLLECTION = "qdrant basics"


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "qdrant_stage5"

client = QdrantClient(path=str(DB_PATH))

if client.collection_exists(COLLECTION):
    client.delete_collection(COLLECTION)

client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(
        size=3,
        distance=Distance.COSINE,
    )
)

points = [
    PointStruct(
        id=1,
        vector=[0.95, 0.10, 0.02],
        payload={"topic": "python", "text": "Python programming"},
    ),
    PointStruct(
        id=2,
        vector=[0.88, 0.15, 0.03],
        payload={"topic": "backend", "text": "Backend development"},
    ),
    PointStruct(
        id=3,
        vector=[0.05, 0.20, 0.95],
        payload={"topic": "database", "text": "Database concepts"},
    ),
]

client.upsert(
    collection_name=COLLECTION,
    points=points,
)

print("Vectors inserted!")

results = client.query_points(
    collection_name=COLLECTION,
    query=[0.92, 0.08, 0.05],
    limit=3,
    with_payload=True,
)
for point in results.points:
    print(f"ID: {point.id}")
    print(f"Score: {point.score:.4f}")
    print(f"Payload: {point.payload}")
    print("-" * 30)


client.close()