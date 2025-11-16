from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import save_contract
from schemas import ContractCreate, ContractOut
from service import analyze_and_store_multimodal
from utils.file_saver import save_upload_file, calculate_file_hash
from models import Contract
from typing import List
import os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/contracts", response_model=List[ContractOut])
def get_all_contracts_endpoint(db: Session = Depends(get_db)):
    """Get all contracts from database"""
    try:
        contracts = db.query(Contract).order_by(Contract.id.desc()).all()
        return contracts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contracts/{contract_id}", response_model=ContractOut)
def get_contract(contract_id: int, db: Session = Depends(get_db)):
    """Get a specific contract by ID"""
    try:
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        return contract
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/contracts/{contract_id}")
def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    """Delete a contract by ID and remove the physical file"""
    try:
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        file_path = os.path.join("contracts", contract.filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as file_error:
                print(f"Warning: Could not delete file {file_path}: {file_error}")

        db.delete(contract)
        db.commit()
        return {"message": "Contract deleted successfully", "deleted_file": contract.filename}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze", response_model=ContractOut)
def analyze_contract(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename_only = file.filename
    temp_path = os.path.join("contracts", filename_only)

    save_upload_file(file, temp_path)
    file_hash = calculate_file_hash(temp_path)

    existing = db.query(Contract).filter_by(file_hash=file_hash).first()
    if existing:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return existing

    try:
        # New parallel, multimodal image processing strategy
        result = analyze_and_store_multimodal(temp_path)

        contract_data = ContractCreate(
            filename=file.filename,
            file_hash=file_hash,
            company_name=result.get("Company Name", ""),
            address=result.get("Address", ""),
            services=result.get("Services provided by the company", {}),
            costing=result.get("Costing of services provided by company", {}),
            signer=result.get("Who has signed the contract", {}),
            end_date=result.get("Expiry / Termination / End Date of contract", ""),
            termination_clause=result.get("Termination Clause of the contract", "")
        )

        saved = save_contract(db, contract_data)
        return saved

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))