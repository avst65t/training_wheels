from fastapi import HTTPException
from .config import logger
from ..db.database import get_rules_from_mongodb


def doc_identify(text):
    try:
        prompt_rules = get_rules_from_mongodb({'prompt': "prompt_1"})
        if not prompt_rules:
            raise HTTPException(status_code=500, detail=f"No rules in the database!")

        prompt = f"""
ROLE: {prompt_rules['role']}

INSTRUCTIONS
{prompt_rules['instructions']}

{prompt_rules['context']}
Context: {text}

EXAMPLE FORMAT:
{prompt_rules['example_format']}"""
        return prompt

    except Exception as e:
        logger.error(f"Error identification documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document identification failed: {str(e)}")


def split_prompt(text, document_types):
    try:
        prompt_rules = get_rules_from_mongodb({'prompt': "prompt_2"})
        if not prompt_rules:
            raise HTTPException(status_code=500, detail=f"No rules in the database!")

        prompt = f"""
ROLE: {prompt_rules['role']}

DOCUMENT TYPES:
{document_types}

INSTRUCTIONS
{prompt_rules['instructions']}

{prompt_rules['context']}
Context: {text}

EXAMPLE FORMAT (purely for your reference and understanding):
{prompt_rules['example_format']}"""
    
        return prompt

    except Exception as e:
        logger.error(f"Error splitting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document splitting failed: {str(e)}")


def extraction_prompt(text, doc_type):
    try:
        rules = get_rules_from_mongodb({'rules': doc_type})
        prompt_rules=get_rules_from_mongodb({'prompt': "prompt_3"})

        prompt = f"""
ROLE: {prompt_rules['role']}

Here are the parameters to extract:
{rules['extraction_rules']}

INSTRUCTIONS
{prompt_rules['instructions']}

{prompt_rules['context']}
Context: {text}

EXAMPLE FORMAT (purely for your reference and understanding):
{prompt_rules['example_format']}"""

        return prompt

    except Exception as e:
        logger.error(f"Error extraction documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document extraction failed: {str(e)}")


def summary_prompt(text, extracted_data, type_doc):
    try:
        prompt_rules = get_rules_from_mongodb({'prompt': "prompt_4"})
        if not prompt_rules:
            raise HTTPException(status_code=500, detail=f"No rules in the database!")
        
        prompt = f"""
ROLE: {prompt_rules['role']}

This is the type of doc:
{type_doc}

These parameters are already extracted. 
{extracted_data}

INSTRUCTIONS
{prompt_rules['instructions']}

{prompt_rules['context']}
Context: {text}

EXAMPLE FORMAT (purely for your reference and understanding):
{prompt_rules['example_format']}"""
    
        return prompt

    except Exception as e:
        logger.error(f"Error summarization documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document summarization failed: {str(e)}")
