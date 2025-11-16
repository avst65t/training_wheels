import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()


async def setup_mongodb():  
    MONGODB_URL = os.getenv("MONGODB_URL")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    rules_collection = db["document_rules"]
    prompt_collection=db["prompt_collection"]
    
    document_rules = [
        {
            "document_type": "NDA",
            "extraction_rules": "Identify all parties bound by confidentiality. Extract definition of confidential information. Find duration of confidentiality obligations. Identify permitted disclosures and exceptions. Extract return or destruction of information clauses",
        },
        {
            "document_type": "MSA",
            "extraction_rules": "Company Name which is providing services. Address of that company. Services provided by that company. Costing of services provided by that company. Also include total estimated annual cost and payment terms. Who has signed the contract (both client and company representative). End Date of contract: Only if clearly labeled. Termination Clause of the contract",
        },
        {
            "document_type": "SOW",
            "extraction_rules": "Extract detailed scope of work and deliverables. Identify project timeline and milestones. Find acceptance criteria and procedures. Extract resource allocation and responsibilities. Identify change management procedures",
        },
        {
            "document_type": "PSA",
            "extraction_rules": "Extract professional services description. Identify consultant qualifications and credentials. Find service level agreements and metrics. Extract fee structure and billing terms. Identify professional standards and compliance",
        }
    ]


    stored_prompts = [
        {
            "prompt_name": "prompt_1",
                "role": "You are a document classification analyst.",
                "instructions": "Analyze the following document text and determine its type. The possible types are:\n- NDA (Non-Disclosure Agreement)\n- MSA (Master Service Agreement)\n- SOW (Statement of Work)\n- PSA (Professional Services Agreement)\n\nAlso check if the document contains multiple document types within it. Only consider NDA, MSA, SOW, PSA as valid document types. Check whether multiple types exist in the document.",
                "context": "You will be provided a raw document. Your job is to identify its type and determine if it contains more than one contract type. For example,(for your reference and understanding only) SoW in MSA document",
                
                "example_format": """{{
    "primary_type": "document_type",
    "has_multiple_types": true/false,
    "detected_types": ["type1", "type2"],
    "confidence": *how confident are you in float}}""",

        },
        {
        "prompt_name": "prompt_2",
            "role": "You are a document structure separator.",
            "instructions": "Please identify the exact starting & ending sentences, punctuations for each document type so they can be separated using regex. Return your response in the JSON format as shown in example format. Each section must have a clear start and end sentence. Do not assume section boundaries - use exact words and punctuation from text.",
            "context": "You have to carefully analyze and act based on the following context",
            
            "example_format": """{{
"splits": [
    {{
        "document_type": "NDA",
        "start_sentence": "exact starting sentence of NDA section",
        "end_sentence": "exact ending sentence of NDA section"
    }},
    {{
        "document_type": "SOW",
        "start_sentence": "exact starting sentence of SOW section",
        "end_sentence": "exact ending sentence of SOW section"
    }}
]
}}
""",
        },
        {
        "prompt_name": "prompt_3",
            "role": "You are a legal document analyzer.",
            "instructions": "For each parameter, If the parameter contains multiple items (e.g., a list of services, pricing breakdowns, or multiple signatories), return them as a structured list or dictionary, not as a flat string. Use meaningful labels or keys if possible (e.g., 'Cloud Management', 'Software Development'). If only one value exists, you may return a string. Always include the **source_sentence** exactly as in the contract (do not paraphrase or add any unecessary symbol). Keep formatting, punctuation, and bullet points as-is in the source sentence. Do not invent or summarize values. Extract only what's in the text. Never merge unrelated items into one string. Always use lists or dictionaries when structure is implied by formatting or commas. Use structured output **only when appropriate**. Do not wrap single values in arrays or dicts unless required",
            "context": "You have to carefully analyze and act based on the following context",
            
            "example_format": """Use this output JSON format:
{
"extracted_parameters": {
      "company_name": {
        "value": "",
        "source_sentence": ""
      },
      "services_provided": {
        "value": {
          "": [],
        },
        "source_sentence": ""
      },
      "costing_of_services": {
        "value": {
          "": {
          "": ""},
        },
      "source_sentence": ""
      },
      "termination_clause": ""
        "source_sentence": ""
      }
  """,
        },

        {"prompt_name": "prompt_4",
        "role": "You are a senior contract analyst preparing an executive summary.",
        "instructions": """Your task is to create an insightful summary of a legal contract
DO NOT mention already extracted parameters in your summary. Focus only on additional insightful content in the document.
Summarize hidden insights, fine print, and clauses that may be important but were not extracted earlier
Use a clean, bullet-point format, grouped under dynamic sections based on what the document contains. 
Do not hardcode section titles, generate them based on actual content
Use clear and simple business/legal language. The tone should be executive and direct — no generic phrases like “this document includes...”.
Keep it structured, insightful, and skimmable, think like a contract analyst preparing notes for leadership.""",
  "context": "You have to carefully analyze and act based on the following context",

  "example_format": """
Legal Framework
*detailed insightful bullet pointers*

Confidentiality
*detailed insightful bullet pointers*

SLAs & Performance
*detailed insightful bullet pointers*

Annexes
*detailed insightful bullet pointers*
"""
}

    ]

    
    try:
        await rules_collection.delete_many({})
        await prompt_collection.delete_many({})

        result = await rules_collection.insert_many(document_rules)
        p_result = await prompt_collection.insert_many(stored_prompts)

        print(f"Successfully inserted {len(result.inserted_ids)} document rule sets")
        print(f"Successfully inserted {len(p_result.inserted_ids)} document rule sets")
        
        # Create indexes for better performance
        await rules_collection.create_index("document_type")
        await prompt_collection.create_index("prompt_name")
        print("Created index on document_type field")
        
        # Verify insertion
        count = await rules_collection.count_documents({})
        print(f"Total document rules in database: {count}")

        p_count = await prompt_collection.count_documents({})
        print(f"Total document rules in database: {p_count}")

    except Exception as e:
        print(f"Error setting up MongoDB: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    print("Setting up MongoDB with document processing rules...")
    asyncio.run(setup_mongodb())
    print("MongoDB setup completed!")


# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")
# db = client["document_rules"]
# collection = db["prompt_collection"]
# for doc in collection.find():
#     print(doc)
