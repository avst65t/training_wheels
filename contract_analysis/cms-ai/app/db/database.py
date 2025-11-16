from fastapi import HTTPException
from ..core.config import db, logger

def get_rules_from_mongodb(data):
    try:
        if 'rules' in data:
            rules_collection = db["document_rules"]
            rules = rules_collection.find_one({"document_type": data['rules'].upper()})
            if not rules:
                raise HTTPException(status_code=500, detail=f"No rules in the database!")
            return rules

        elif 'prompt' in data:
            prompt_collection = db["prompt_collection"]
            p_rules = prompt_collection.find_one({"prompt_name": data['prompt']})
            if not p_rules:
                raise HTTPException(status_code=500, detail=f"No rules in the database!")            
            return p_rules            

    except Exception as e:
        logger.error(f"Error fetching rules from MongoDB: {str(e)}")
        raise HTTPException(status_code=500, detail=f"DB issue!")
