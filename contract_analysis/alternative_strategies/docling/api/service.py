# service.py
from data_extraction import parse_document_with_docling
from chunking import chunk_contract
from llm_model import extract_fields_from_text
from post_process import merge_field_outputs

def analyze_and_store(file_path: str) -> dict:
    print('doc to be parsed')
    full_text = parse_document_with_docling(file_path)
    print('doc parsed')

    if len(full_text) > 60000:
        chunks = chunk_contract(full_text)
        outputs = [extract_fields_from_text(chunk) for chunk in chunks]
    else:
        print('openai')
        outputs = [extract_fields_from_text(full_text)]
        print('openai done')

    merged = merge_field_outputs(outputs)
    print('fields merged, json made', merged)
    return merged