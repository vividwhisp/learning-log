import re

def split_markdown_sections(text: str) -> list[dict]:
    sections = []
    current_heading = []
    current_content = []

    for line in text.splitlines():
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)

        if heading_match:
            if current_content:
                sections.append({
                    "heading": " > ".join(current_heading),
                    "text":"\n".join(current_content).strip(),
                })
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()

            current_heading = current_heading[:level - 1]
            current_heading.append(title)
            current_content = [line]
        else:
            current_content.append(line)
    if current_content:
        sections.append({
            "heading": " > ".join(current_heading),
            "text": "\n".join(current_content).strip(),
        })
    return sections

def split_blocks(text: str) -> list[dict]:
    blocks = []
    current = []
    in_code_block = False

    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
        current.append(line)

        if not in_code_block and not line.strip():
            block = "\n".join(current).strip()

            if block:
                blocks.append(block)
            current = []
    if current:
        block = "\n".join(current).strip()
        if block:
            blocks.append(block)
    return blocks

def assemble_chunks(blocks: list[str], chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Require chunk_size > overlap >= 0")
    chunks = []
    current = ""

    for block in blocks:
        candidate = f"{current}\n\n{block}".strip() if current else block
        if len(candidate) <= chunk_size:
            current = candidate 
            continue

        if current:
            chunks.append(current)
        if len(block) > chunk_size:
            chunks.extend(
                split_oversized_block(block, chunk_size, overlap)
            )
            current = ""
        else:
            current = current[-overlap:] + "\n\n" + block if overlap else block

    if current:
        chunks.append(current)

    return chunks

def split_oversized_block(
    block: str,
    chunk_size: int,
    overlap: int,
) -> list[str]:
    lines = block.splitlines()
    chunks = []
    current = []

    for line in lines:
        candidate = "\n".join(current + [line])

        if len(candidate) <= chunk_size:
            current.append(line)
            continue

        if current:
            chunks.append("\n".join(current))

        # Retain previous lines within the overlap budget.
        previous = []
        overlap_length = 0

        for old_line in reversed(current):
            added_length = len(old_line) + (1 if previous else 0)

            if overlap_length + added_length > overlap:
                break

            previous.insert(0, old_line)
            overlap_length += added_length

        current = previous

        if len(line) > chunk_size:
            # Single extremely long line: character-level fallback.
            start = 0

            while start < len(line):
                end = min(start + chunk_size, len(line))
                chunks.append(line[start:end])

                if end == len(line):
                    break

                start = end - overlap

            current = []
        else:
            current.append(line)

    if current:
        chunks.append("\n".join(current))

    return chunks