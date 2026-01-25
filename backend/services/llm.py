from groq import Groq
from utils.prompts import SYSTEM_PROMPT
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def process_with_llm(text: str):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text[:8000]}  # avoid token overflow
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    return json.loads(content)
