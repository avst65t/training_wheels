import json
from ..core.prompt import doc_identify, split_prompt, extraction_prompt, summary_prompt
from fastapi import HTTPException
from ..utils.util import get_llm_response
from ..core.config import logger
from llama_index.core import SimpleDirectoryReader
from typing import List


def extract_text_from_file(file_path):
    try:
        reader = SimpleDirectoryReader(input_files=[file_path])
        documents = reader.load_data()
        if not documents:
            raise ValueError("No content extracted from file!")
            
        full_text = "\n".join([doc.text for doc in documents])
        return full_text
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")
    

def identify_document_type(text):
    try:
        prompt = doc_identify(text)
        response = get_llm_response(prompt, model="gpt-4.1-nano", temperature=0)
        result = json.loads(response)
        return result
        
    except Exception as e:
        logger.error(f"Error identifying document type: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document type identification failed: {str(e)}")


def split_multiple_documents(text: str, document_types: List[str]):
    try:
        prompt = split_prompt(text, document_types)
        response = get_llm_response(prompt, model="gpt-4.1-mini", temperature=0)
        result = json.loads(response)
        return result["splits"]

    except Exception as e:
        logger.error(f"Error splitting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document splitting failed: {str(e)}")


def extract_parameters_from_chunk(text, doc_type):
    try:
        prompt = extraction_prompt(text, doc_type)
        response = get_llm_response(prompt, model="gpt-4.1-mini", temperature=0)
        result = json.loads(response)
        return result

    except Exception as e:
        logger.error(f"Error extracting parameters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


def generate_summary(text, extracted_data, type_doc) -> str:
    try:
        prompt = summary_prompt(text, extracted_data, type_doc)
        response = get_llm_response(prompt, model="gpt-4.1-nano", temperature=0.3)
        return response
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return "Summary generation failed"


# from llama_index.core.node_parser import TokenTextSplitter
# def chunk_text(text: str, chunk_size: int) -> List[str]:
#     if len(text) <= chunk_size:
#         return [text]
#     try:
#         chunk_overlap = int(chunk_size * 0.05)
#         text_splitter = TokenTextSplitter(
#             chunk_size=chunk_size,
#             chunk_overlap=chunk_overlap,
#             separator="\n\n",
#             backup_separators=["\n"],
#         )
#         return text_splitter.split_text(text)
#     except Exception as e:
#         logger.error(f"Error with LlamaIndex splitter: {e}")
#         raise HTTPException(status_code=500, detail=f"Text chunking failed: {str(e)}")
