from pathlib import Path
from qdrant_client import QdrantClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "qdrant_stage5"

client = QdrantClient(path=str(DB_PATH))

print("Qdrant Initialization")