"""
CarbonTrace AI
FastAPI Routes

Provides API endpoints for:

- Health check
- Lyzr status
- PDF upload and processing
- Emission calculation
- Audit records
- Compliance and greenwashing checks
"""

from pathlib import Path
import os
import re
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
)

from backend.services.document_processor import (
    process_document
)


router = APIRouter()


# ---------------------------------------------------------
# UPLOAD DIRECTORY
# ---------------------------------------------------------

UPLOAD_DIR = Path(
    "sample_data/uploads"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# COMPLIANCE CHECKER
# ---------------------------------------------------------

def build_compliance_results(
    records: list,
    document_text: str,
) -> dict:
    """
    Build compliance and greenwashing findings.

    Important:

    - Calculations remain deterministic.
    - Scope classification remains controlled
      by Python rules.
    - Emission factors come from the configured
      factor dataset.
    - AI is not allowed to invent numerical results.
    """

    findings = []


    # -----------------------------------------------------
    # 1. Calculation integrity
    # -----------------------------------------------------

    calculation_valid = True

    for record in records:

        expected = (
            record["quantity"]
            * record["emission_factor"]
        )

        actual = record[
            "emissions_kg_co2e"
        ]

        if abs(
            expected - actual
        ) > 0.000001:

            calculation_valid = False
            break


    if calculation_valid:

        findings.append({

            "type":
                "CALCULATION_INTEGRITY",

            "status":
                "PASS",

            "severity":
                "LOW",

            "message": (
                "CO2e calculations were performed "
                "deterministically using activity data "
                "and configured emission factors."
            ),

        })

    else:

        findings.append({

            "type":
                "CALCULATION_INTEGRITY",

            "status":
                "FAIL",

            "severity":
                "HIGH",

            "message": (
                "One or more emission calculations "
                "do not match the configured "
                "calculation formula."
            ),

        })


    # -----------------------------------------------------
    # 2. Scope validation
    # -----------------------------------------------------

    valid_scopes = {
        1,
        2,
        3,
    }

    scopes_valid = all(

        record["scope"]
        in valid_scopes

        for record in records

    )


    if scopes_valid:

        findings.append({

            "type":
                "SCOPE_CLASSIFICATION",

            "status":
                "PASS",

            "severity":
                "LOW",

            "message": (
                "All emission activities were assigned "
                "to valid Scope 1, Scope 2, or Scope 3 "
                "categories using controlled business rules."
            ),

        })

    else:

        findings.append({

            "type":
                "SCOPE_CLASSIFICATION",

            "status":
                "FAIL",

            "severity":
                "HIGH",

            "message": (
                "One or more activities have an invalid "
                "emission scope."
            ),

        })


    # -----------------------------------------------------
    # 3. Emission factor traceability
    # -----------------------------------------------------

    factors_available = all(

        record.get(
            "emission_factor"
        ) is not None

        for record in records

    )


    if factors_available:

        findings.append({

            "type":
                "EMISSION_FACTOR_TRACEABILITY",

            "status":
                "PASS",

            "severity":
                "LOW",

            "message": (
                "Every calculated activity has a configured "
                "emission factor and factor unit."
            ),

        })

    else:

        findings.append({

            "type":
                "EMISSION_FACTOR_TRACEABILITY",

            "status":
                "FAIL",

            "severity":
                "HIGH",

            "message": (
                "One or more activities are missing "
                "an emission factor."
            ),

        })


    # -----------------------------------------------------
    # 4. Missing activity data
    # -----------------------------------------------------

    if len(records) == 0:

        findings.append({

            "type":
                "DATA_COMPLETENESS",

            "status":
                "FAIL",

            "severity":
                "HIGH",

            "message": (
                "No emission activities were detected "
                "in the uploaded document."
            ),

        })

    else:

        findings.append({

            "type":
                "DATA_COMPLETENESS",

            "status":
                "PASS",

            "severity":
                "LOW",

            "message": (
                f"{len(records)} emission activity "
                "record(s) were successfully extracted "
                "and processed."
            ),

        })


    # -----------------------------------------------------
    # 5. Greenwashing claim detection
    # -----------------------------------------------------

    text = (
        document_text or ""
    ).lower()


    claim_patterns = [

        r"\bcarbon\s+neutral\b",

        r"\bnet\s+zero\b",

        r"\bzero\s+emission[s]?\b",

        r"\b100%\s+green\b",

        r"\bfully\s+green\b",

        r"\bemission[-\s]?free\b",

    ]


    detected_claims = []


    for pattern in claim_patterns:

        matches = re.findall(
            pattern,
            text
        )


        for match in matches:

            clean_match = (
                match.strip()
            )


            if clean_match not in detected_claims:

                detected_claims.append(
                    clean_match
                )


    if detected_claims:

        findings.append({

            "type":
                "GREENWASHING_CLAIM",

            "status":
                "REVIEW",

            "severity":
                "MEDIUM",

            "message": (
                "Environmental claims were detected "
                "in the document. These claims should "
                "be supported by verifiable evidence "
                "before being presented as compliance "
                "or sustainability statements."
            ),

            "claims":
                detected_claims,

            "activities":
                [],

        })

    else:

        findings.append({

            "type":
                "GREENWASHING_CLAIM",

            "status":
                "PASS",

            "severity":
                "LOW",

            "message": (
                "No common high-risk environmental "
                "marketing claims were detected "
                "in the uploaded document."
            ),

            "claims":
                [],

            "activities":
                [],

        })


    # -----------------------------------------------------
    # Overall risk
    # -----------------------------------------------------

    high_risk = any(

        finding["severity"] == "HIGH"

        and

        finding["status"] == "FAIL"

        for finding in findings

    )


    medium_risk = any(

        finding["severity"] == "MEDIUM"

        and

        finding["status"] == "REVIEW"

        for finding in findings

    )


    if high_risk:

        overall_risk = "HIGH"

    elif medium_risk:

        overall_risk = "REVIEW"

    else:

        overall_risk = "LOW"


    return {

        "overall_risk":
            overall_risk,

        "findings":
            findings,

    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@router.get("/health")
def health_check():
    """
    Check whether the CarbonTrace API is running.
    """

    return {

        "status":
            "ok",

        "service":
            "CarbonTrace AI",

    }


# ---------------------------------------------------------
# LYZR STATUS
# ---------------------------------------------------------

@router.get("/lyzr-status")
def lyzr_status():
    """
    Check whether Lyzr is configured and enabled.

    This endpoint does NOT expose the API key.
    """

    api_key_configured = bool(
        os.getenv("LYZR_API_KEY")
    )


    lyzr_enabled = (
        os.getenv(
            "CARBONTRACE_USE_LYZR",
            "false"
        )
        .strip()
        .lower()
        in {
            "true",
            "1",
            "yes",
            "on",
        }
    )


    if (
        api_key_configured
        and lyzr_enabled
    ):

        status = "READY"

    elif api_key_configured:

        status = "CONFIGURED_BUT_DISABLED"

    elif lyzr_enabled:

        status = "ENABLED_BUT_KEY_MISSING"

    else:

        status = "NOT_CONFIGURED"


    return {

        "lyzr_api_key_configured":
            api_key_configured,

        "lyzr_enabled":
            lyzr_enabled,

        "status":
            status,

    }


# ---------------------------------------------------------
# PDF UPLOAD + PROCESSING
# ---------------------------------------------------------

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):
    """
    Upload a PDF and process its emission data.
    """

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )


    if not file.filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )


    file_path = (
        UPLOAD_DIR /
        file.filename
    )


    try:

        # -----------------------------------------
        # Save uploaded PDF
        # -----------------------------------------

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # -----------------------------------------
        # Process document
        # -----------------------------------------

        result = process_document(
            str(file_path)
        )


        return {

            "success":
                True,

            "filename":
                file.filename,

            "activity_count":
                result[
                    "activity_count"
                ],

            "extraction_engine":
                result.get(
                    "extraction_engine",
                    "unknown"
                ),

            "audit_records":
                result[
                    "audit_records"
                ],

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
    Upload a PDF and return:

    - Total emissions
    - Scope 1
    - Scope 2
    - Scope 3
    - Emission records
    - Compliance findings
    - Extraction engine
    """

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )


    if not file.filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )


    file_path = (
        UPLOAD_DIR /
        file.filename
    )


    try:

        # -------------------------------------------------
        # Save uploaded file
        # -------------------------------------------------

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # -------------------------------------------------
        # Process document
        # -------------------------------------------------

        result = process_document(
            str(file_path)
        )


        records = result[
            "audit_records"
        ]


        # -------------------------------------------------
        # Scope calculations
        # -------------------------------------------------

        scope_1 = sum(

            record[
                "emissions_kg_co2e"
            ]

            for record in records

            if record[
                "scope"
            ] == 1

        )


        scope_2 = sum(

            record[
                "emissions_kg_co2e"
            ]

            for record in records

            if record[
                "scope"
            ] == 2

        )


        scope_3 = sum(

            record[
                "emissions_kg_co2e"
            ]

            for record in records

            if record[
                "scope"
            ] == 3

        )


        # -------------------------------------------------
        # Total emissions
        # -------------------------------------------------

        total = (

            scope_1
            + scope_2
            + scope_3

        )


        # -------------------------------------------------
        # Compliance
        # -------------------------------------------------

        compliance = (
            build_compliance_results(

                records,

                result[
                    "text"
                ],

            )
        )


        # -------------------------------------------------
        # Final API response
        # -------------------------------------------------

        return {

            "success":
                True,

            "filename":
                file.filename,

            "extraction_engine":
                result.get(
                    "extraction_engine",
                    "unknown"
                ),

            "total_kg_co2e":
                total,

            "scope_1_kg_co2e":
                scope_1,

            "scope_2_kg_co2e":
                scope_2,

            "scope_3_kg_co2e":
                scope_3,

            "records":
                records,

            "compliance":
                compliance,

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

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )


    if not file.filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )


    file_path = (
        UPLOAD_DIR /
        file.filename
    )


    try:

        # -----------------------------------------
        # Save PDF
        # -----------------------------------------

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # -----------------------------------------
        # Process document
        # -----------------------------------------

        result = process_document(
            str(file_path)
        )


        return {

            "success":
                True,

            "filename":
                file.filename,

            "extraction_engine":
                result.get(
                    "extraction_engine",
                    "unknown"
                ),

            "audit_trail":
                result[
                    "audit_records"
                ],

        }


    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error),

        )