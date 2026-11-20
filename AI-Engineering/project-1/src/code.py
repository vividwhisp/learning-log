#code practice file
def filter_results(results : list[dict], source : str) -> list[dict]:
    filtered = []
    if not results:
        return []
    for result in results:
        if result["source"] == source:
            filtered.append(result)
    return filtered

filtered = filter_results([
    {"title": "Pods", "source": "kubernetes.md"},
    {"title": "Indexes", "source": "postgresql.md"},
    {"title": "Services", "source": "kubernetes.md"},
],"kubernetes.md")

print(filtered)

def count_results_by_source(results : list[dict]) -> dict:
    source_counts = {}
    for result in results:
        if result["source"] in source_counts:
            source_counts[result["source"]] += 1
        else:
            source_counts[result["source"]] = 1
    return source_counts

source_count = count_results_by_source([
    {"title": "Pods", "source": "kubernetes.md"},
    {"title": "Indexes", "source": "postgresql.md"},
    {"title": "Services", "source": "kubernetes.md"},
])

print(source_count)