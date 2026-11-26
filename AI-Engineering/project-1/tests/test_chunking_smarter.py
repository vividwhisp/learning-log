from src.structured_chunker import chunk_markdown

with open("data/documents/kubernetes.md", "r", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_markdown(text)

print("Total chunks:", len(chunks))

# for i, chunk in enumerate(chunks):
#     print(f"\nCHUNK {i + 1} (length={len(chunk['text'])})")
#     print("Title:", chunk["document_title"])
#     print("Heading:", chunk["heading"])
#     print(repr(chunk["text"][:150]))

for i, chunk in enumerate(chunks):
    text = chunk["text"]
    fence_count = text.count("```")

    print(
        f"Chunk {i + 1}: "
        f"length={len(text)}, "
        f"fences={fence_count}, "
        f"balanced={fence_count % 2 == 0}"
    )