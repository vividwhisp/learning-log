import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHUNKS_FILE = PROJECT_ROOT / "data" / "chunks.json"

def main():
    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    for chunk in chunks:
        print("\n" + "=" * 70)
        print(f"Source: {chunk["source"]}")
        print(f"Chunk index: {chunk["chunk_index"]}")
        print(f"Title: {chunk["title"]}")
        print("-" * 70)
        print(chunk["text"])

if __name__ == "__main__":
    main()