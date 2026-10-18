# Python Fundamentals for Backend and Data Applications

## Python's Role in an Application

Python is a general-purpose programming language used for automation, APIs, data processing, machine learning, and developer tools. A Python program is commonly organized into modules and packages. A module is usually a `.py` file, while a package groups related modules under a directory. Clear module boundaries make code easier to test, reuse, and maintain.

Python uses dynamic typing, but variables still refer to objects with particular types. Type hints describe expected inputs and outputs and help editors, reviewers, and static-analysis tools understand a program. Type hints do not automatically validate arbitrary runtime data; validation requires explicit checks or a library designed for that purpose.

```python
from collections.abc import Sequence


def average(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)
```

The annotation communicates that `average` expects a sequence of numbers and returns a float. The explicit empty-sequence check prevents division by zero and makes the failure understandable to callers.

## Virtual Environments and Dependencies

A virtual environment isolates a project's installed Python packages from other projects and the system Python installation. This helps avoid dependency conflicts. Create one with `python -m venv .venv` and activate it using the command appropriate for your shell. Install dependencies with the environment's Python interpreter, for example `python -m pip install fastapi`, so the package installer corresponds to the interpreter being used.

A project should record its direct dependencies in a dependency file such as `requirements.txt` or in the project's chosen packaging configuration. Reproducible deployments require deliberate dependency versions and a documented installation process. The `.venv` directory, local secrets, bytecode caches, and other generated files generally should not be committed to Git.

Useful commands include:

```bash
python --version
python -m venv .venv
python -m pip install -r requirements.txt
python -m pip show fastapi
python -m pip freeze
```

`python -m pip show` reports information about a package installed for the selected interpreter. If an editor reports that an import cannot be resolved, check which interpreter the editor uses before reinstalling packages. The terminal and editor can point to different environments.

## Functions, Collections, and Data Structures

Functions package behavior into reusable units. Use descriptive names, keep functions focused, and return values instead of relying on unexpected global state. A list is ordered and mutable, a tuple is ordered and immutable, a dictionary maps keys to values, and a set stores unique elements. Choosing a suitable data structure improves both clarity and performance.

```python
documents = [
    {"id": "doc-1", "title": "Kubernetes Basics", "text": "A Pod is a deployable unit."},
    {"id": "doc-2", "title": "PostgreSQL Basics", "text": "A transaction groups database operations."},
]

by_id = {document["id"]: document for document in documents}
print(by_id["doc-1"]["title"])
```

The dictionary comprehension builds an index by document ID. A dictionary lookup is generally more appropriate than scanning a list repeatedly when many lookups by the same key are needed.

## Reading Files Safely

Use a context manager when opening files. It ensures that the file is closed even if processing raises an exception. Specify an encoding for text files so behavior is consistent across environments. When recursively loading documents, filter by the intended file extension and handle missing directories or unreadable files explicitly.

```python
from pathlib import Path


def read_markdown(path: Path) -> str:
    if path.suffix.lower() != ".md":
        raise ValueError(f"Expected a Markdown file: {path}")
    return path.read_text(encoding="utf-8")
```

`pathlib.Path` offers cross-platform path handling. Keeping file discovery separate from parsing makes an ingestion pipeline easier to test: one function can discover files, another can read content, and another can turn content into chunks with metadata.

## Exceptions and Resource Cleanup

Exceptions represent errors or unusual conditions that a caller may need to handle. Catch specific exceptions when recovery is possible, and avoid broad `except Exception` blocks that silently hide programming defects. Include useful context in error messages, but do not log passwords, access tokens, or other secrets.

```python
from pathlib import Path


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Document does not exist: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"Document is not valid UTF-8 text: {path}") from exc
```

The `raise ... from exc` syntax preserves the original exception as the cause, which helps debugging. Use `finally` or context managers when a resource must be cleaned up; context managers are the usual choice for files and many database connections.

## Testing with pytest

Automated tests check that code behaves as expected and help prevent regressions. Unit tests should verify normal cases, edge cases, and failure cases. For a chunking function, useful cases include empty input, a short document, text longer than the chunk limit, heading boundaries, and a final chunk that is shorter than the others.

```python
def split_text(text: str, max_chars: int) -> list[str]:
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]


def test_split_text_preserves_all_characters() -> None:
    source = "abcdefgh"
    chunks = split_text(source, max_chars=3)
    assert chunks == ["abc", "def", "gh"]
    assert "".join(chunks) == source
```

This simple splitter uses fixed character lengths and may cut through words or Markdown structures; a production ingestion pipeline may instead prefer paragraph- or heading-aware splitting. The test illustrates an important invariant: if the chosen strategy is intended to preserve the complete source text, concatenating its chunks should reproduce the input exactly.

## HTTP APIs with FastAPI

FastAPI is a Python framework for building HTTP APIs. A route maps an HTTP method and path to a Python function. Pydantic models can validate and parse request data. Keep input validation, business logic, and persistence sufficiently separated that they can be tested independently.

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    limit: int = Field(default=5, ge=1, le=20)


@app.post("/search")
def search(request: SearchRequest) -> dict[str, object]:
    return {"query": request.query, "limit": request.limit, "results": []}
```

This is only a minimal endpoint skeleton; it validates the request but does not perform semantic retrieval. A search service would embed the query, request nearest vectors from a vector database, and serialize the matching document metadata and scores. An API should return predictable errors and avoid exposing internal stack traces or secrets to clients.

## Logging and Configuration

Use the `logging` module instead of sprinkling `print` calls throughout a long-running service. Include enough information to diagnose a problem, such as an operation name, request identifier, or document ID, while avoiding unnecessary personal data and secrets. Configure log levels by environment so development can be more verbose than production.

Read environment-specific settings from environment variables or a configuration system. Do not commit real `.env` files containing secrets. A `.env.example` file can document required variable names with placeholder values. Configuration should be validated at startup when missing or malformed values would prevent the application from working correctly.

## Practical Engineering Guidelines

Prefer small functions with clear contracts, meaningful variable names, and explicit error handling. Separate I/O from pure transformation logic where possible. For an ingestion system, file reading and database writes are I/O, while normalization, chunk construction, and metadata validation can often be tested as deterministic transformations. Store source identifiers and chunk indices so retrieved passages can be traced back to their original documents. Add tests before making the pipeline more complex, and document setup commands so another developer can reproduce the project locally.
