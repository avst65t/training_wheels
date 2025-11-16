from sqlalchemy import Column, Integer, String, JSON
from database import Base
from sqlalchemy import Text

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)        # just for display
    file_hash = Column(String, unique=True, index=True)  # used to check duplicates
    company_name = Column(String, index=True)
    address = Column(Text)
    services = Column(JSON)
    costing = Column(JSON)
    signer = Column(JSON)
    end_date = Column(String)
    termination_clause = Column(Text)
