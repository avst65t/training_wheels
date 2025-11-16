from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import save_contract, get_all_contracts
from schemas import ContractCreate, ContractOut
from service import analyze_and_store
from utils.file_saver import save_upload_file
import os
from utils.file_saver import save_upload_file, calculate_file_hash
from models import Contract
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
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
        
        # Delete the physical file if it exists
        file_path = os.path.join("contracts", contract.filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as file_error:
                print(f"Warning: Could not delete file {file_path}: {file_error}")
                # Continue with database deletion even if file deletion fails
        
        # Delete from database
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
        result = analyze_and_store(temp_path)

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


# result = {'Company Name': 'TechNova Solutions Inc.', 
#           'Address': '123 Innovation Drive, Silicon Valley, CA 94025, United States', 
#           'Services provided by the company': 
#             {'Cloud Infrastructure Management': ['24/7 monitoring of AWS/Azure cloud environments', 'Monthly performance optimization reports', 'Disaster recovery setup and testing'], 
#             'Software Development': ['Custom ERP system development (Python/Django)', 'Quarterly feature updates and bug fixes'], 
#             'Data Analytics': ['BI dashboard development (Power BI/Tableau)', 'Monthly data processing and insights reports'], 
#             'Support & Maintenance': ['Dedicated helpdesk (8 AM-8 PM EST, Mon-Fri)', 'SLA: 99.9% uptime guaranteed']}, 
#         'Costing of services provided by company': {'Cloud Management': {'Cost (Monthly)': '$12,000', 'Billing Cycle': 'Quarterly'}, 'Software Development': {'Cost (Monthly)': '$45,000', 'Billing Cycle': 'Milestone-based'}, 'Data Analytics': {'Cost (Monthly)': '$8,500', 'Billing Cycle': 'Monthly'}, 'Support &Maintenance': {'Cost (Monthly)': '$6,200', 'Billing Cycle': 'Annual'}, 'Total Estimated Annual Cost': '$862,400', 'Payment Terms': 'Net 30 days, late fees of 1.5% per month'}, 
#         'Who has signed the contract': {'Company': {'Name': 'John A. Smith', 'Title': 'CEO'}, 'Client': {'Name': 'Emily R. Johnson', 'Title': 'COO'}}, 
#         'Expiry / Termination / End Date of contract': 'January 14, 2028 (3-year term)', 
#         'Termination Clause of the contract': 'Termination Conditions:\n\n- 1. By Client: 90-day written notice with $25,000 early termination fee\n- 2. By Company: Only for non-payment (>60 days overdue)\n- 3. Automatic Renewal: 1-year extensions unless terminated 60 days prior to expiry'}


# {'Company Name': 'TechNova Solutions Inc.', 
# 'Address': '123 Innovation Drive, Silicon Valley, CA 94025, United States', 
# 'Services provided by the company': '1. Cloud Infrastructure Management - 24/7 monitoring of AWS/Azure cloud environments - Monthly performance optimization reports - Disaster recovery setup and testing 2. Software Development - Custom ERP system development (Python/Django) - Quarterly feature updates and bug fixes 3. Data Analytics - BI dashboard development (Power BI/Tableau) - Monthly data processing and insights reports 4. Support & Maintenance - Dedicated helpdesk (8 AM-8 PM EST, Mon-Fri) - SLA: 99.9% uptime guaranteed', 
# 'Costing of services provided by company': 'Cloud Management: $12,000 monthly, Software Development: $45,000 monthly, Data Analytics: $8,500 monthly, Support & Maintenance: $6,200 monthly, Total Estimated Annual Cost: $862,400', 
# 'Who has signed the contract': 'John A. Smith (CEO, TechNova Solutions Inc.)', 
# 'Expiry / Termination / End Date of contract': 'January 14, 2028', 
# 'Termination Clause of the contract': '1. By Client: 90-day written notice with $25,000 early termination fee\n2. By Company: Only for non-payment (>60 days overdue)\n3. Automatic Renewal: 1-year extensions unless terminated 60 days prior to expiry\n\nPost-Termination Obligations:\n- Data handover within 30 days\n- Final invoice payable immediately'}
