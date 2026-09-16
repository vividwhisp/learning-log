from pydantic import BaseModel #type: ignore
import os
from openai import OpenAI #type: ignore
from dotenv import load_dotenv #type: ignore

load_dotenv()
class Explanation(BaseModel):
    topic: str
    difficulty: str
    summary: str


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

response = client.responses.parse(
    model="openai/gpt-oss-20b",
    input="Explain recursion to a beginner",
    text_format=Explanation
)

result = response.output_parsed

print(result)