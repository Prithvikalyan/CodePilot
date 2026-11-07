
from openai import OpenAI

from app.config import (
    NVIDIA_API_KEY,
    NVIDIA_MODEL,
    NVIDIA_BASE_URL,
)

if not NVIDIA_API_KEY:
    raise ValueError("NVIDIA_API_KEY is missing from .env")


client = OpenAI(
    api_key=NVIDIA_API_KEY,
    base_url=NVIDIA_BASE_URL,
    timeout=120.0,
    max_retries=2,
)


def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=NVIDIA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=4096,
    )

    message = response.choices[0].message

    print("\n--- LLM DEBUG ---")
    print("Finish reason:", response.choices[0].finish_reason)
    print("Content:", message.content)
    print("Reasoning:", getattr(message, "reasoning", None))
    print("-----------------\n")

    if message.content is None:
        raise ValueError(
            "NVIDIA returned an empty message content."
        )

    return message.content
    