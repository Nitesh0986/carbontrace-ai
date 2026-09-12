"""
CarbonTrace AI
Document Processing Service

Runs the complete document-to-audit workflow.

PDF
 ↓
Text Extraction
 ↓
Activity Extraction
 ↓
Emission Processing
 ↓
Audit Records
"""

from backend.services.pdf_ingestion import extract_text_from_pdf
from backend.services.agent_interface import extract_activities_with_agent
from backend.services.batch_processor import process_activity_records


def process_document(file_path: str) -> dict:
    """
    Process a PDF document from start to finish.

    Returns:
        A dictionary containing the extracted text,
        number of activities, and audit records.
    """

    # 1. Extract raw text from PDF
    text = extract_text_from_pdf(file_path)

    # 2. Extract structured activities
    activities = extract_activities_with_agent(text)

    # 3. Process activities through deterministic pipeline
    audit_records = process_activity_records(activities)

    return {
        "text": text,
        "activity_count": len(activities),
        "audit_records": audit_records,
    }