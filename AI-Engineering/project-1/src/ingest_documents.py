import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCS_DIR = PROJECT_ROOT / "data" / "documents"
OUTPUT_FILE = PROJECT_ROOT / "data" / "chunks.json"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

def extract_title(text: str, file_path: Path) -> str:
    """Ue the first Markdown H1 as the title, if avaialbale"""
    match = re.search(r"^\s*#\s+(.+)$", text, re.MULTILINE)
    if match:
        return match.group(1).strip()

    return file_path.stem.replace("-", " ").title()

def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """Split text into approximately chunk_size characters with overlap."""
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    if not text:
        return []

    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Require chunk_size > overlap >= 0")

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        # Prefer ending at a paragraph boundary when possible.
        if end < len(text):
            boundary = text.rfind("\n\n", start + chunk_size // 2, end)

            if boundary != -1:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        # Carry some previous text into the next chunk for context.
        start = max(end - overlap, start + 1)

    return chunks


def ingest_documents() -> list[dict]:
    if not DOCS_DIR.exists():
        raise FileNotFoundError(
            f"Documents directory not found: {DOCS_DIR}"
        )

    files = sorted(DOCS_DIR.glob("*.md"))

    if not files:
        raise FileNotFoundError(
            f"No Markdown files found in {DOCS_DIR}"
        )

    records = []

    for file_path in files:
        text = file_path.read_text(encoding="utf-8")
        title = extract_title(text, file_path)
        chunks = chunk_text(text)

        print(f"{file_path.name}: {len(chunks)} chunks")

        for index, chunk in enumerate(chunks):
            records.append(
                {
                    "id": f"{file_path.stem}-{index:03d}",
                    "title": title,
                    "source": file_path.name,
                    "chunk_index": index,
                    "text": chunk,
                }
            )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"\nTotal chunks: {len(records)}")
    print(f"Saved to: {OUTPUT_FILE}")

    return records


if __name__ == "__main__":
    ingest_documents()