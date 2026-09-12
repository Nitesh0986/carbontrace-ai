"""
CarbonTrace AI
FastAPI Routes

Provides API endpoints for:
- Health check
- PDF upload and processing
- Emission calculation
- Audit records
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from backend.services.document_processor import process_document


router = APIRouter()


# Temporary upload directory
UPLOAD_DIR = Path("sample_data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@router.get("/health")
def health_check():
    """
    Check whether the CarbonTrace API is running.
    """

    return {
        "status": "ok",
        "service": "CarbonTrace AI",
    }


# ---------------------------------------------------------
# PDF UPLOAD + PROCESSING
# ---------------------------------------------------------

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF and process its emission data.
    """

    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    # Create file path
    file_path = UPLOAD_DIR / file.filename

    try:
        # Save uploaded PDF
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process document
        result = process_document(str(file_path))

        return {
            "success": True,
            "filename": file.filename,
            "activity_count": result["activity_count"],
            "audit_records": result["audit_records"],
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ---------------------------------------------------------
# EMISSIONS SUMMARY
# ---------------------------------------------------------

@router.post("/emissions")
async def calculate_emissions_from_pdf(
    file: UploadFile = File(...)
):
    """
    Upload a PDF and return emission summary.
    """

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    file_path = UPLOAD_DIR / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = process_document(str(file_path))

        records = result["audit_records"]

        scope_1 = sum(
            record["emissions_kg_co2e"]
            for record in records
            if record["scope"] == 1
        )

        scope_2 = sum(
            record["emissions_kg_co2e"]
            for record in records
            if record["scope"] == 2
        )

        scope_3 = sum(
            record["emissions_kg_co2e"]
            for record in records
            if record["scope"] == 3
        )

        total = scope_1 + scope_2 + scope_3

        return {
            "success": True,
            "filename": file.filename,
            "total_kg_co2e": total,
            "scope_1_kg_co2e": scope_1,
            "scope_2_kg_co2e": scope_2,
            "scope_3_kg_co2e": scope_3,
            "records": records,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ---------------------------------------------------------
# AUDIT TRAIL
# ---------------------------------------------------------

@router.post("/audit")
async def get_audit_trail(
    file: UploadFile = File(...)
):
    """
    Upload a PDF and return complete audit records.
    """

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    file_path = UPLOAD_DIR / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = process_document(str(file_path))

        return {
            "success": True,
            "filename": file.filename,
            "audit_trail": result["audit_records"],
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )