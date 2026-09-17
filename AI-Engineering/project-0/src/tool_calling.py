import os
from dotenv import load_dotenv #type: ignore
from openai import OpenAI #type: ignore
import json

load_dotenv()

client = OpenAI(
    api_key = os.getenv("GROQ_API_KEY"),
    base_url = "https://api.groq.com/openai/v1",
)

def calculate(a: float, b: float, operation: str) -> float:
    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        return a / b

    raise ValueError("Unknown operation")

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a mathematical calculation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number.",
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number.",
                    },
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide",
                        ],
                        "description": "The mathematical operation to perform.",
                    },
                },
                "required": ["a", "b", "operation"],
            },
        },
    }
]


response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages = [
       { "role": "user",
        "content" : "What is 137 multiplied by 24?",
       }
    ],
    tools=tools,
)

tool_call = response.choices[0].message.tool_calls[0]
print("Tool call: ",tool_call.function.name)
print("Args: ", tool_call.function.arguments)

arguments = json.loads(tool_call.function.arguments)
result = calculate(**arguments)

messages = [
    {
        "role": "user",
        "content": "What is 137 multiplied by 24? explain in one sentence and break it down in detail",
    }
]

messages.append(response.choices[0].message)
messages.append(
    {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(result),
    }
)

final_response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    tools=tools,
)

print(final_response.choices[0].message.content)