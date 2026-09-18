import os
from dotenv import load_dotenv #type: ignore
from openai import OpenAI #type: ignore
from fastapi import FastAPI #type: ignore
from pydantic import BaseModel #type: ignore

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role" : "user",
                "content": request.message,
            }
        ],
        
    )
    return {
            "response" : response.choices[0].message.content
            }