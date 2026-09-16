import os
import sys
from dotenv import load_dotenv  # type: ignore
from openai import OpenAI  # type: ignore

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set")

client = OpenAI(api_key=api_key,
                base_url="https://api.groq.com/openai/v1")
while True:
    user_input = input("You: ")
    if user_input == "exit":
        print("Exiting..")
        sys.exit()
    else:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            temperature=0.7,
            messages=[
               {"role":"user","content":user_input }
            ],
            max_tokens=1024
        )
        ai_response = response.choices[0].message.content
        print(f"AI: {ai_response}" )