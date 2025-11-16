from pydantic import BaseModel
from typing import Optional, Dict, List, Any


class ContractCreate(BaseModel):
    filename: str
    file_hash: str

    # Use exact keys as in your prompt
    company_name: Optional[str] = ""
    address: Optional[str] = ""

    # Free-form dictionaries (still structured but not strictly typed)
    services: Optional[Dict[str, List[str]]] = None
    costing: Optional[Dict[str, Any]] = None  # Includes sub-services + total + terms

    signer: Optional[Dict[str, Dict[str, str]]] = None  # Company/Client => Name/Title

    end_date: Optional[str] = ""
    termination_clause: Optional[str] = ""


class ContractOut(ContractCreate):
    id: int

    class Config:
        orm_mode = True
