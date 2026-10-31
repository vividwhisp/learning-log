import re

def extract_citations(answer: str, results : list[dict]) -> list[dict]:
    cited_indices = {
        int(index)
        for index in re.findall(
            r"[【\[]\s*Source\s+(\d+)\s*[】\]]",
            answer,
        )
    }
    sources = []

    for index in sorted(cited_indices):
        if 1 <= index <= len(results):
            result = results[index - 1]

            sources.append({
                "title" : result["title"],
                "source" : result["source"],
                "chunk_index" : result["chunk_index"],
                "text" : result["text"],
            })
    return sources