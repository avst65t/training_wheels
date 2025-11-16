import re
import tiktoken
from openai import OpenAI
from fastapi import HTTPException
from ..core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_llm_response(prompt, model, temperature):
    try:
        response = client.responses.create(
                    model=model,
                    input=prompt,
                    temperature=temperature,)
        return response.output_text
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM call failed: {str(e)}")


def count_tokens(text: str):
    encoding = tiktoken.get_encoding("o200k_base")
    tokens = encoding.encode(text)
    return len(tokens)


def save_extracted_text(full_text):
    with open('extracted_text.txt', 'w', encoding='utf-8') as file:
        file.write(full_text)


def split_doc(splits, full_text, doc_to_process):
    for split in splits:
        start_pattern = re.escape(split["start_sentence"])
        end_pattern = re.escape(split["end_sentence"])
        pattern = f"{start_pattern}(.*?){end_pattern}"
        match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
        
        if match:
            split_text = split["start_sentence"] + match.group(1) + split["end_sentence"]
            doc_to_process.append({
                "type": split["document_type"],
                "text": split_text
            })
    return doc_to_process