# crud.py
from sqlalchemy.orm import Session
from models import Contract
from schemas import ContractCreate

def save_contract(db: Session, contract: ContractCreate) -> Contract:
    db_contract = Contract(**contract.dict())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def get_all_contracts(db: Session):
    return db.query(Contract).all()