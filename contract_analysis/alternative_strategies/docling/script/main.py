from utils import merge_field_outputs
from data_extraction import parse_document_with_docling
from chunking import chunk_contract
from llm_model import extract_fields_from_text
from storage import save_text_to_file

def process_contracts(file_path: str):
    print('starting analysis')
    full_text = parse_document_with_docling(file_path)
    # contracts = split_into_contracts(full_text)
    # all_results = []
    save_text_to_file(full_text, "simple_document.txt")
    print('text extracted')
    # for idx, contract in enumerate(contracts, start=1):
    if len(full_text) > 60000:
        chunks = chunk_contract(full_text)
        outputs = [extract_fields_from_text(chunk) for chunk in chunks]
    else:
        outputs = [extract_fields_from_text(full_text)]

    print('text analyzed!')
    merged = merge_field_outputs(outputs)
    # all_results.append({"contract_id": idx, **merged})
    return merged

if __name__ == "__main__":
    path = 'x.pdf'
    results = process_contracts(path)
    print('\n\n', results)
