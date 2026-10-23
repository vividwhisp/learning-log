
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from src.search import SemanticSearch


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the model and Qdrant once at startup.
    app.state.searcher = SemanticSearch()

    try:
        yield
    finally:
        app.state.searcher.close()


app = FastAPI(
    title="Technical Knowledge Search API",
    description="Semantic search over technical documentation.",
    version="1.0.0",
    lifespan=lifespan,
)


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    limit: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    title: str
    source: str
    chunk_index: int | None
    text: str
    score: float


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: list[SearchResult]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search", response_model=SearchResponse)
def search_documents(
    body: SearchRequest,
    request: Request,
):
    if not body.query.strip():
        raise HTTPException(
            status_code=422,
            detail="Query cannot be empty or whitespace.",
        )

    searcher = request.app.state.searcher

    results = searcher.search(
        query=body.query,
        limit=body.limit,
    )

    return SearchResponse(
        query=body.query,
        total_results=len(results),
        results=results,
    )
