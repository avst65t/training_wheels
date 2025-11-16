# parallel_processor.py
import asyncio
import base64
import aiofiles
from prompts import build_prompt_for_image
from openai import AsyncOpenAI

client = AsyncOpenAI()

FIELD_PROMPT = build_prompt_for_image()

async def encode_image_base64(image_path):
    async with aiofiles.open(image_path, "rb") as f:
        return base64.b64encode(await f.read()).decode("utf-8")

async def extract_single_page_data(image_path: str) -> dict:
    print(image_path)
    base64_img = await encode_image_base64(image_path)
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an expert contract analyst."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": FIELD_PROMPT},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_img}"}}
                    ]
                }
            ],
            temperature=0.1,
            max_tokens=2000
        )
        content = response.choices[0].message.content
        return eval(content) if content else {}
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return {}

async def extract_data_from_pages_parallel(image_paths: list) -> list:
    tasks = [extract_single_page_data(path) for path in image_paths]
    return await asyncio.gather(*tasks)

def extract_data_from_pages_parallel_sync(image_paths: list) -> list:
    return asyncio.run(extract_data_from_pages_parallel(image_paths))
