import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import build_prompt

load_dotenv()
client=OpenAI()
openai_api_key = os.getenv("OPENAI_API_KEY")

def extract_fields_from_text(text: str) -> dict:
    prompt = build_prompt(text)
    print('\nPrompt:\n'+prompt+'\n\n')

    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[
            {"role": "system", "content": "You extract structured contract data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=2048
)
    return response.choices[0].message.content
