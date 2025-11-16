from pydantic import BaseModel
from typing import List, Dict, Any

class ContractCreate(BaseModel):
    filename: str
    file_hash: str
    company_name: str
    address: str
    services: Any
    costing: Any
    signer: Any
    end_date: str
    termination_clause: str

class ContractOut(ContractCreate):
    id: int

    class Config:
        orm_mode = True
