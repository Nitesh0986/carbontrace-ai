"""
CarbonTrace AI
FastAPI Routes

Features:

- Health check
- Lyzr status
- PDF ingestion
- CSV ingestion
- Deterministic CO2e calculation
- Scope classification
- Factor provenance
- Audit trail
- Greenwashing detection
- Data quality scoring
- Disclosure readiness
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

from backend.services.csv_document_processor import (
    process_csv_document
)


router = APIRouter()


# =========================================================
# UPLOAD DIRECTORY
# =========================================================

UPLOAD_DIR = Path(
    "sample_data/uploads"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# GREENWASHING CHECK
# =========================================================

def detect_greenwashing(
    records: list,
    document_text: str,
) -> dict:
    """
    Detect potentially unsupported environmental claims.

    This is a deterministic compliance guardrail.

    Important:
    The system does not decide that a company is
    actually fraudulent. It flags claims that require
    evidence before publication.
    """

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

        r"\bclimate\s+positive\b",

    ]

    detected_claims = []

    for pattern in claim_patterns:

        matches = re.findall(
            pattern,
            text
        )

        for match in matches:

            claim = match.strip()

            if claim not in detected_claims:

                detected_claims.append(
                    claim
                )

    # ---------------------------------------------
    # No environmental claim
    # ---------------------------------------------

    if not detected_claims:

        return {

            "type":
                "GREENWASHING_CLAIM",

            "status":
                "PASS",

            "severity":
                "LOW",

            "decision":
                "ALLOWED",

            "message": (
                "No high-risk environmental "
                "marketing claim was detected."
            ),

            "claims":
                [],

        }

    # ---------------------------------------------
    # Claim exists
    # ---------------------------------------------

    has_activity_evidence = (
        len(records) > 0
    )

    has_factor_evidence = all(
        record.get("emission_factor") is not None
        and record.get("factor_source")
        for record in records
    )

    # A strong claim without supporting
    # quantified evidence is blocked.
    if not has_activity_evidence:

        return {

            "type":
                "GREENWASHING_CLAIM",

            "status":
                "BLOCKED",

            "severity":
                "HIGH",

            "decision":
                "BLOCKED",

            "message": (
                "Environmental claim detected, "
                "but no quantified emission evidence "
                "was found in the supplied document."
            ),

            "claims":
                detected_claims,

        }

    if not has_factor_evidence:

        return {

            "type":
                "GREENWASHING_CLAIM",

            "status":
                "BLOCKED",

            "severity":
                "HIGH",

            "decision":
                "BLOCKED",

            "message": (
                "Environmental claim detected, "
                "but supporting emission-factor "
                "evidence is incomplete."
            ),

            "claims":
                detected_claims,

        }

    # Evidence exists, but human review
    # is still required before publication.
    return {

        "type":
            "GREENWASHING_CLAIM",

        "status":
            "REVIEW",

        "severity":
            "MEDIUM",

        "decision":
            "REVIEW_REQUIRED",

        "message": (
            "Environmental claim detected. "
            "Quantified emission evidence exists, "
            "but the claim should still be reviewed "
            "before publication."
        ),

        "claims":
            detected_claims,

    }


# =========================================================
# DATA QUALITY SCORE
# =========================================================

def calculate_data_quality(
    records: list,
) -> dict:
    """
    Calculate a deterministic data-quality score.

    Checks:

    - Activity
    - Quantity
    - Unit
    - Context
    - Scope
    - Emission factor
    - Factor source
    - Calculation validation
    """

    if not records:

        return {

            "score": 0,

            "grade": "FAIL",

            "checks": {

                "activity": False,

                "quantity": False,

                "unit": False,

                "context": False,

                "scope": False,

                "emission_factor": False,

                "factor_source": False,

                "calculation_validation": False,

            },

        }

    total_points = 0
    earned_points = 0

    check_names = [

        "activity",
        "quantity",
        "unit",
        "context",
        "scope",
        "emission_factor",
        "factor_source",
        "calculation_validation",

    ]

    checks = {}

    for record in records:

        record_checks = {

            "activity":
                bool(
                    record.get("activity")
                ),

            "quantity":
                record.get("quantity") is not None
                and record.get("quantity") >= 0,

            "unit":
                bool(
                    record.get("unit")
                ),

            "context":
                bool(
                    record.get("context")
                ),

            "scope":
                record.get("scope")
                in {1, 2, 3},

            "emission_factor":
                record.get(
                    "emission_factor"
                ) is not None,

            "factor_source":
                bool(
                    record.get(
                        "factor_source"
                    )
                ),

            "calculation_validation":
                record.get(
                    "validation_status"
                ) == "PASS",

        }

        for name in check_names:

            total_points += 1

            if record_checks[name]:

                earned_points += 1

        # Aggregate check:
        # true only if every record passes.
        for name in check_names:

            previous = checks.get(
                name,
                True
            )

            checks[name] = (
                previous
                and record_checks[name]
            )

    score = round(
        (
            earned_points
            / total_points
        ) * 100
    )

    if score >= 90:

        grade = "EXCELLENT"

    elif score >= 75:

        grade = "GOOD"

    elif score >= 50:

        grade = "REVIEW"

    else:

        grade = "FAIL"

    return {

        "score":
            score,

        "grade":
            grade,

        "checks":
            checks,

    }


# =========================================================
# FACTOR EVIDENCE SUMMARY
# =========================================================

def build_factor_evidence(
    records: list,
) -> list:
    """
    Build judge-friendly factor evidence records.
    """

    evidence = []

    for record in records:

        evidence.append({

            "activity":
                record.get(
                    "activity"
                ),

            "factor":
                record.get(
                    "emission_factor"
                ),

            "factor_unit":
                record.get(
                    "factor_unit"
                ),

            "scope":
                record.get(
                    "scope"
                ),

            "source":
                record.get(
                    "factor_source",
                    "Unknown"
                ),

            "year":
                record.get(
                    "factor_year"
                ),

            "methodology":
                record.get(
                    "factor_methodology",
                    "Unknown"
                ),

            "region":
                record.get(
                    "factor_region",
                    "Unknown"
                ),

            "status":
                record.get(
                    "factor_status",
                    "unknown"
                ),

        })

    return evidence


# =========================================================
# COMPLIANCE ENGINE
# =========================================================

def build_compliance_results(
    records: list,
    document_text: str,
) -> dict:
    """
    Build complete compliance results.
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

        actual = (
            record["emissions_kg_co2e"]
        )

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
                "One or more calculations do not "
                "match the deterministic formula."
            ),

        })

    # -----------------------------------------------------
    # 2. Scope validation
    # -----------------------------------------------------

    scopes_valid = all(

        record.get("scope")
        in {1, 2, 3}

        for record in records

    )

    findings.append({

        "type":
            "SCOPE_CLASSIFICATION",

        "status":
            "PASS"
            if scopes_valid
            else "FAIL",

        "severity":
            "LOW"
            if scopes_valid
            else "HIGH",

        "message": (

            "All activities have valid "
            "Scope 1, 2 or 3 classifications."

            if scopes_valid

            else

            "One or more activities have "
            "an invalid emission scope."

        ),

    })

    # -----------------------------------------------------
    # 3. Factor traceability
    # -----------------------------------------------------

    factor_traceable = all(

        record.get(
            "emission_factor"
        ) is not None

        and record.get(
            "factor_source"
        )

        for record in records

    )

    findings.append({

        "type":
            "EMISSION_FACTOR_TRACEABILITY",

        "status":
            "PASS"
            if factor_traceable
            else "FAIL",

        "severity":
            "LOW"
            if factor_traceable
            else "HIGH",

        "message": (

            "Every emission calculation has "
            "factor provenance."

            if factor_traceable

            else

            "One or more calculations lack "
            "factor provenance."

        ),

    })

    # -----------------------------------------------------
    # 4. Data completeness
    # -----------------------------------------------------

    data_complete = (
        len(records) > 0
    )

    findings.append({

        "type":
            "DATA_COMPLETENESS",

        "status":
            "PASS"
            if data_complete
            else "FAIL",

        "severity":
            "LOW"
            if data_complete
            else "HIGH",

        "message": (

            f"{len(records)} emission activity "
            "record(s) were processed."

            if data_complete

            else

            "No emission activities were detected."

        ),

    })

    # -----------------------------------------------------
    # 5. Greenwashing
    # -----------------------------------------------------

    greenwashing = detect_greenwashing(
        records,
        document_text,
    )

    findings.append(
        greenwashing
    )

    # -----------------------------------------------------
    # 6. Overall risk
    # -----------------------------------------------------

    blocked = any(

        finding.get("status")
        == "BLOCKED"

        for finding in findings

    )

    high_risk = any(

        finding.get("severity")
        == "HIGH"

        and

        finding.get("status")
        == "FAIL"

        for finding in findings

    )

    medium_risk = any(

        finding.get("severity")
        == "MEDIUM"

        and

        finding.get("status")
        in {
            "REVIEW",
            "BLOCKED",
        }

        for finding in findings

    )

    if blocked or high_risk:

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


# =========================================================
# DISCLOSURE READINESS
# =========================================================

def build_disclosure_readiness(
    records: list,
    compliance: dict,
    quality: dict,
) -> dict:
    """
    Build a structured disclosure-readiness summary.

    This is NOT a legal certification.

    It is a review-support layer.
    """

    scope_1 = sum(

        record[
            "emissions_kg_co2e"
        ]

        for record in records

        if record.get("scope") == 1

    )

    scope_2 = sum(

        record[
            "emissions_kg_co2e"
        ]

        for record in records

        if record.get("scope") == 2

    )

    scope_3 = sum(

        record[
            "emissions_kg_co2e"
        ]

        for record in records

        if record.get("scope") == 3

    )

    total = (
        scope_1
        + scope_2
        + scope_3
    )

    risk = compliance[
        "overall_risk"
    ]

    ready = (

        len(records) > 0

        and quality["score"] >= 75

        and risk == "LOW"

    )

    return {

        "status":
            "READY_FOR_REVIEW"
            if ready
            else "REVIEW_REQUIRED",

        "scope_1_kg_co2e":
            scope_1,

        "scope_2_kg_co2e":
            scope_2,

        "scope_3_kg_co2e":
            scope_3,

        "total_kg_co2e":
            total,

        "data_quality_score":
            quality["score"],

        "compliance_risk":
            risk,

        "legal_disclaimer": (
            "Disclosure-readiness support only. "
            "Final CSRD/SEC reporting decisions "
            "require appropriate human and professional review."
        ),

    }


# =========================================================
# HEALTH
# =========================================================

@router.get("/health")
def health_check():

    return {

        "status":
            "ok",

        "service":
            "CarbonTrace AI",

    }


# =========================================================
# LYZR STATUS
# =========================================================

@router.get("/lyzr-status")
def lyzr_status():

    api_key_configured = bool(
        os.getenv(
            "LYZR_API_KEY"
        )
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

        status = (
            "CONFIGURED_BUT_DISABLED"
        )

    elif lyzr_enabled:

        status = (
            "ENABLED_BUT_KEY_MISSING"
        )

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


# =========================================================
# MAIN PROCESSING ENDPOINT
# PDF + CSV
# =========================================================

@router.post("/emissions")
async def calculate_emissions(
    file: UploadFile = File(...)
):
    """
    Process PDF or CSV emission data.
    """

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    filename = (
        file.filename
        .lower()
    )

    supported = (
        filename.endswith(".pdf")
        or filename.endswith(".csv")
    )

    if not supported:

        raise HTTPException(

            status_code=400,

            detail=(
                "Only PDF and CSV files "
                "are supported."
            ),

        )

    file_path = (
        UPLOAD_DIR
        / file.filename
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
        # Process according to file type
        # -------------------------------------------------

        if filename.endswith(".pdf"):

            result = process_document(
                str(file_path)
            )

        else:

            result = process_csv_document(
                str(file_path)
            )

        records = result[
            "audit_records"
        ]

        # -------------------------------------------------
        # Scope totals
        # -------------------------------------------------

        scope_1 = sum(

            record[
                "emissions_kg_co2e"
            ]

            for record in records

            if record.get("scope") == 1

        )

        scope_2 = sum(

            record[
                "emissions_kg_co2e"
            ]

            for record in records

            if record.get("scope") == 2

        )

        scope_3 = sum(

            record[
                "emissions_kg_co2e"
            ]

            for record in records

            if record.get("scope") == 3

        )

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

                result.get(
                    "text",
                    ""
                ),

            )
        )

        # -------------------------------------------------
        # Data quality
        # -------------------------------------------------

        quality = (
            calculate_data_quality(
                records
            )
        )

        # -------------------------------------------------
        # Factor evidence
        # -------------------------------------------------

        factor_evidence = (
            build_factor_evidence(
                records
            )
        )

        # -------------------------------------------------
        # Disclosure readiness
        # -------------------------------------------------

        disclosure = (
            build_disclosure_readiness(

                records,

                compliance,

                quality,

            )
        )

        # -------------------------------------------------
        # Return complete response
        # -------------------------------------------------

        return {

            "success":
                True,

            "filename":
                file.filename,

            "file_type":
                "pdf"
                if filename.endswith(".pdf")
                else "csv",

            "extraction_engine":
                result.get(
                    "extraction_engine",
                    "unknown"
                ),

            "activity_count":
                result[
                    "activity_count"
                ],

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

            "factor_evidence":
                factor_evidence,

            "compliance":
                compliance,

            "data_quality":
                quality,

            "disclosure_readiness":
                disclosure,

        }

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error),

        )


# =========================================================
# SIMPLE UPLOAD ENDPOINT
# =========================================================

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    filename = (
        file.filename.lower()
    )

    if not (
        filename.endswith(".pdf")
        or filename.endswith(".csv")
    ):

        raise HTTPException(

            status_code=400,

            detail=(
                "Only PDF and CSV files "
                "are supported."
            ),

        )

    file_path = (
        UPLOAD_DIR
        / file.filename
    )

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        if filename.endswith(".pdf"):

            result = process_document(
                str(file_path)
            )

        else:

            result = process_csv_document(
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
                    "extraction_engine"
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


# =========================================================
# AUDIT ENDPOINT
# =========================================================

@router.post("/audit")
async def get_audit_trail(
    file: UploadFile = File(...)
):

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
        UPLOAD_DIR
        / file.filename
    )

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

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