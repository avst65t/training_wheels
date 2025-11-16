# from datetime import datetime
# from typing import Optional
# from pydantic import BaseModel, EmailStr, Field
# from .mongo_ids import PyObjectId


# class User(BaseModel):
#     _id: Optional[PyObjectId] = Field(default=None)
#     email: Optional[EmailStr] = None
#     password: Optional[str] = None
#     role: Optional[str] = None
#     deletedAt: Optional[datetime] = None
#     createdAt: datetime = Field(default_factory=datetime.utcnow)
#     updatedAt: datetime = Field(default_factory=datetime.utcnow)

#     class Config:
#         json_encoders = {PyObjectId: str}
#         arbitrary_types_allowed = True


# from pydantic import BaseModel
# class ExtractedParameter(BaseModel):
#     parties_involved: List[Dict[str, str]]
#     contract_dates: Dict[str, Dict[str, str]]
#     termination_clause: Dict[str, str]
#     signatories: List[Dict[str, str]]
#     services_provided: Dict[str, str]
#     key_terms: List[Dict[str, str]]
#     risks_and_obligations: List[Dict[str, str]]

# class ProcessingResult(BaseModel):
#     document_type: str
#     has_multiple_types: bool
#     extracted_parameters: ExtractedParameter
#     summary: str
#     status: str
    
# class DocumentSplit(BaseModel):
#     start_sentence: str
#     end_sentence: str
#     document_type: str
