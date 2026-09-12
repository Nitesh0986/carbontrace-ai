"""
CarbonTrace AI
Document Processing Service

Pipeline:

PDF
 ↓
Text Extraction
 ↓
AI Activity Extraction
 ↓
Activity Normalization
 ↓
Deterministic Emission Processing
 ↓
Audit Trail
"""

from pathlib import Path

from backend.services.pdf_ingestion import (
    extract_text_from_pdf
)

from backend.services.agent_interface import (
    extract_activities_with_agent,
    should_use_lyzr,
)

from backend.services.batch_processor import (
    process_activity_records
)


def process_document(file_path: str) -> dict:
    """
    Process an ESG PDF document from start to finish.
    """

    # -----------------------------------------
    # 1. Extract text from PDF
    # -----------------------------------------

    text = extract_text_from_pdf(
        file_path
    )


    # -----------------------------------------
    # 2. Decide extraction engine
    # -----------------------------------------

    use_lyzr = should_use_lyzr()


    # -----------------------------------------
    # 3. Extract emission activities
    # -----------------------------------------

    activities = extract_activities_with_agent(
        text=text,
        use_lyzr=use_lyzr,
    )


    # -----------------------------------------
    # 4. Source document name
    # -----------------------------------------

    source_document = Path(
        file_path
    ).name


    # -----------------------------------------
    # 5. Deterministic processing
    # -----------------------------------------

    audit_records = process_activity_records(
        activities,
        source_document=source_document,
    )


    # -----------------------------------------
    # 6. Return complete result
    # -----------------------------------------

    return {
        "text": text,

        "activity_count":
            len(activities),

        "extraction_engine":
            "lyzr"
            if use_lyzr
            else "local",

        "audit_records":
            audit_records,
    }