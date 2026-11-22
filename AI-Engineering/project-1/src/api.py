import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Header, Depends
from pydantic import BaseModel, Field

from src.reranked_search import RerankedSearch
from src.generation import generate_rag_answer
from src.citations import extract_citations
from src.logger import get_logger
from groq import(
    APIConnectionError,
    APITimeoutError,
    APIStatusError,
    AuthenticationError,
    RateLimitError,
)

logger = get_logger(__name__)


def get_current_tenant(x_demo_user: str = Header(default="")) -> str:
    demo_users = {
        "alice-demo-token" : "alice_001",
        "bob-demo-token": "bob_001",
    }

    tenant_id = demo_users.get(x_demo_user)

    if tenant_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing demo identity. ",
        )

    return tenant_id

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing search services")
    # Initialize the model and Qdrant once at startup.
    app.state.searcher = RerankedSearch()
    logger.info("Search services initialized successfully")
    try:
        yield
    finally:
        logger.info("Shutting down search services")
        app.state.searcher.close()
        logger.info("Search services shut down")


app = FastAPI(
    title="Technical Knowledge Search API",
    description="Semantic search over technical documentation.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.middleware("http")
async def measure_request_time(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s | Status: %s | Duration: %.2f ms",
        request.method,
        request.url.path,
        response.status_code,
        elapsed,
    )
    return response

class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    limit: int = Field(default=5, ge=1, le=20)
    source: str | None = None


class SearchResult(BaseModel):
    title: str
    source: str | None = Field(default=None, min_length=1)
    chunk_index: int | None
    text: str
    retrieval_score : float
    rerank_score : float


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: list[SearchResult]

class SourceCitation(BaseModel):
    title: str
    source: str
    chunk_index: int | None
    text: str


class AskResponse(BaseModel):
    query: str
    answer: str
    sources: list[SourceCitation]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search", response_model=SearchResponse)
def search_documents(
    body: SearchRequest,
    request: Request,
    tenant_id: str = Depends(get_current_tenant),
):
    if not body.query.strip():
        raise HTTPException(
            status_code=422,
            detail="Query cannot be empty or whitespace.",
        )

    searcher = request.app.state.searcher
    logger.info("Search request received")
    results = searcher.search(
        query=body.query,
        tenant_id=tenant_id,
        limit=body.limit,
        source=body.source,
    )
    logger.info("Search completed. Results found: %d", len(results))
    return SearchResponse(
        query=body.query,
        total_results=len(results),
        results=results,
    )

@app.post("/ask", response_model=AskResponse)
def ask_question(
    body: SearchRequest,
    request: Request,
    tenant_id: str = Depends(get_current_tenant),
):
    if not body.query.strip():
        raise HTTPException(
            status_code=422,
            detail="Query cannot be empty or whitespace.",
        )

    searcher = request.app.state.searcher
    logger.info("Ask request received")
    results = searcher.search(
        query=body.query,
        tenant_id=tenant_id,
        limit=body.limit,
        source=body.source,
    )
    logger.info("Retrieval completed. Results found: %d", len(results))
    if not results:
        return AskResponse(
            query=body.query,
            answer="I couldn't find relevant information in the available documents.",
            sources=[],
        )
    try:
        answer = generate_rag_answer(body.query, results)

    except AuthenticationError:
        raise HTTPException(
            status_code=500,
            detail="AI service configuration error.",
        )
    except RateLimitError:
        raise HTTPException(
            status_code=503,
            detail="AI service request timed out.",
        )
    except APITimeoutError:
        raise HTTPException(
        status_code=504,
        detail="AI service request timed out.",
    )

    except APIConnectionError:
       raise HTTPException(
        status_code=502,
        detail="Could not connect to the AI service.",
        )

    except APIStatusError:
        raise HTTPException(
            status_code=502,
            detail="AI service returned an error.",
        )
    sources = extract_citations(answer, results)
    return AskResponse(
        query=body.query,
        answer=answer,
        sources=sources,
    )

