from .document_processing import extract_text_from_file, identify_document_type, split_multiple_documents, extract_parameters_from_chunk, generate_summary
from ..utils.util import count_tokens, split_doc  #, save_extracted_text
from fastapi.responses import JSONResponse
from fastapi import HTTPException


def start_processing(temp_file_path):
    full_text = extract_text_from_file(temp_file_path)
    token_count = count_tokens(full_text)
    if token_count>45000:
        raise HTTPException(status_code=500, detail=f"Too long pdf! Try shorter one")

    # save_extracted_text(full_text)
    doc_type_info = identify_document_type(full_text)
    documents_to_process = []

    if doc_type_info.get("has_multiple_types", False):
        splits = split_multiple_documents(full_text, doc_type_info["detected_types"])
        documents_to_process=split_doc(splits, full_text, documents_to_process)
    else:
        documents_to_process.append({
            "type": doc_type_info["primary_type"],
            "text": full_text
        })

    all_results = []
    for doc_info in documents_to_process:
        extraction_result = extract_parameters_from_chunk(doc_info['text'], doc_info['type'])
        summary = generate_summary(doc_info['text'], extraction_result, doc_info['type'])
        result = {
            "document_type": doc_info['type'],
            "has_multiple_types": doc_type_info["has_multiple_types"],
            "extracted_parameters": extraction_result,
            "summary": summary,
            "status": "success"}
        
        all_results.append(result)
    return JSONResponse(content=all_results)
