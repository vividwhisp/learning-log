import json
from pathlib import Path

from src.reranked_search import RerankedSearch
from src.generation import generate_rag_answer
from src.citations import extract_citations

ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "eval" /"answer_queries.json"
OUTPUT_PATH = ROOT / "eval" / "answer_results.json"

