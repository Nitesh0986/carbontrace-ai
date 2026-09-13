"""
CarbonTrace AI
CSV Document Processor

Processes CSV activity data through the same
deterministic emission pipeline used by PDF data.
"""

from pathlib import Path

from backend.services.csv_ingestion import load_csv
from backend.services.batch_processor import process_activity_records


def process_csv_document(file_path: str) -> dict:
    """
    Process an activity CSV.

    Pipeline:

    CSV
     ↓
    Structured activity records
     ↓
    Scope classification
     ↓
    Factor matching
     ↓
    Deterministic calculation
     ↓
    Audit trail
    """

    records = load_csv(
        file_path
    )

    source_document = Path(
        file_path
    ).name

    audit_records = process_activity_records(
        records,
        source_document=source_document,
    )

    return {
        "activity_count": len(records),
        "extraction_engine": "csv",
        "text": "",
        "audit_records": audit_records,
    }