import re

def get_overlap(text: str, overlap: int) -> str:
    if overlap == 0:
        return ""

    start = max(0, len(text) - overlap)

    # Move forward to the next whitespace so we don't start mid-word.
    while start < len(text) and not text[start].isspace():
        start += 1

    return text[start:].strip()

def split_markdown_sections(text: str):
    document_title = ""
    sections = []
    heading_stack = []
    current_lines = []

    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)$", line)

        if match:
            level = len(match.group(1))
            heading_text = match.group(2).strip()

            # The H1 is the document title, not a standalone section.
            if level == 1:
                document_title = heading_text
                continue

            # Save the previous section.
            if current_lines:
                sections.append({
                    "heading": " > ".join(heading_stack),
                    "text": "\n".join(current_lines).strip(),
                })
                current_lines = []

            # Keep only the heading hierarchy relevant to this level.
            heading_stack = heading_stack[:level - 2]
            heading_stack.append(heading_text)

        current_lines.append(line)

    # Save the final section.
    if current_lines:
        sections.append({
            "heading": " > ".join(heading_stack),
            "text": "\n".join(current_lines).strip(),
        })

    return document_title, sections

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
            overlap_text = get_overlap(current, overlap)
            current = f"{overlap_text}\n\n{block}".strip() if overlap_text else block
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

def chunk_markdown(text: str):
    document_title, sections = split_markdown_sections(text)
    chunks = []

    for section in sections:
        blocks = split_blocks(section["text"])
        section_chunks = assemble_chunks(blocks)

        for chunk_text in section_chunks:
            if chunk_text.strip():
                chunks.append({
                    "document_title": document_title,
                    "heading": section["heading"],
                    "text": chunk_text.strip()
                })

    return chunks