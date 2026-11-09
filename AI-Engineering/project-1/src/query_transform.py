import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

SYSTEM_PROMPT = """
You are a query rewriting assistant for a technical documentation
retrieval system.

Your task is to rewrite the user's query to improve information retrieval.

Rules:
1. Preserve the original intent and meaning.
2. Preserve technical names, technologies, versions, and constraints.
3. Include useful technical terminology and synonyms where appropriate.
4. Do not invent specific requirements or assumptions.
5. Do not answer the question.
6. Return exactly one concise rewritten search query.
7. Do not include explanations, labels, or quotation marks.
"""


def rewrite_query(query: str) -> str:
    if not query.strip():
        return query

    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        max_completion_tokens=150,
    )

    rewritten_query = response.choices[0].message.content

    if not rewritten_query or not rewritten_query.strip():
        raise RuntimeError("The LLM returned an empty rewritten query.")

    return rewritten_query.strip()