import os
import sys
import time
from dotenv import load_dotenv  # type: ignore
from openai import OpenAI  # type: ignore

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set")

client = OpenAI(api_key=api_key,
                base_url="https://api.groq.com/openai/v1")

TYPING_SPEED = 0.03
while True:
    user_input = input("You: ")
    if user_input.lower().strip() == "exit":
        print("Exiting..")
        sys.exit()
    else:
        stream = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            temperature=0.7,
            messages=[
               {"role":"user","content":user_input }
            ],
            max_tokens=1024,
            stream=True
        )
        
        print("AI: ", end="", flush=True)
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                text_chunk = chunk.choices[0].delta.content
                print(text_chunk,end="",flush=True)
                time.sleep(TYPING_SPEED)
        print()