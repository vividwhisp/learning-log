import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT/".env")

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

SYSTEM_PROMPT = """
You are a multi-query generation assistant for a technical
documentation retrieval system.

Generate alternative search queries for the user's question.

Rules:
1. Preserve the original question's intent.
2. Explore different terminology and retrieval perspectives.
3. Include relevant technical terminology where appropriate.
4. Do not invent requirements or change the question's scope.
5. Do not answer the question.
6. Avoid duplicates and superficial rewordings.
7. Return valid JSON in this exact format:

{
    "queries": [
        "alternative query 1",
        "alternative query 2",
        "alternative query 3"
    ]
}
"""


def generate_queries(query: str, num_queries: int = 3) -> list[str]:
    if not query.strip():
        return []

    if not 1 <= num_queries <= 5:
        raise ValueError("num_queries must be between 1 and 5.")

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY not found in .env.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Generate {num_queries} alternative search queries "
                    f"for this question:\n{query}"
                ),
            },
        ],
        temperature=0.3,
        max_completion_tokens=400,
    )

    content = response.choices[0].message.content

    if not content or not content.strip():
        raise RuntimeError("The LLM returned an empty response.")

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"The LLM returned invalid JSON: {content}"
        ) from exc

    generated = data.get("queries")

    if not isinstance(generated, list):
        raise ValueError("Expected a JSON object containing a queries list.")

    alternatives = []
    seen = {query.strip().casefold()}

    for item in generated:
        if not isinstance(item, str):
            continue

        candidate = item.strip()

        if not candidate:
            continue

        if candidate.casefold() in seen:
            continue

        seen.add(candidate.casefold())
        alternatives.append(candidate)

        if len(alternatives) == num_queries:
            break

    if not alternatives:
        raise RuntimeError("The LLM did not generate valid alternative queries.")

    return alternatives
