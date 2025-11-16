# from fastapi import APIRouter, UploadFile, Depends, status, Form, Query, HTTPException, Body
# from pydantic import BaseModel, Field
# from ..core.security import role_required

from fastapi import APIRouter, UploadFile, status, HTTPException, File
from ..controllers.controller import start_processing
import shutil, tempfile, os
from pathlib import Path

router = APIRouter(tags=["digitization"])

@router.post("/process-document", status_code=status.HTTP_201_CREATED)
def process_document(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix.lower()
    # allowed_extensions = {'.pdf', '.docx', '.txt'}
    # if file_extension not in allowed_extensions:
    #     raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are allowed")
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        final_data = start_processing(temp_file_path)
        return final_data

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
