import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

apikey = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if not apikey:
    raise RuntimeError("GROQ_API_KEY is missing")

client = Groq(api_key=apikey)

response = client.chat.completions.create(
    model=model,
    messages = [
        {
            "role":"system",
            "content":"You are a concise technical tutor",
        },
        {
            "role":"user",
            "content": "Explain semantic search in three sentences.",
        }
    ],
    temperature=0.2,
    max_completion_tokens=200,
)

print(response.choices[0].message.content)


