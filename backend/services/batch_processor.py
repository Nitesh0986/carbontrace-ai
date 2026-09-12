"""
CarbonTrace AI
Batch Emission Processor
"""

from backend.services.emission_pipeline import process_emission
from backend.services.audit_logger import create_audit_record


def process_activity_records(
    records: list,
    source_document: str = "unknown",
) -> list:
    """
    Process multiple ActivityRecord objects
    and create traceable audit records.
    """

    results = []

    for record in records:

        # ---------------------------------------------
        # Deterministic emission processing
        # ---------------------------------------------

        emission_record = process_emission(
            activity=record.activity,
            quantity=record.quantity,
            unit=record.unit,
            context=record.context,
        )

        # ---------------------------------------------
        # Create detailed audit record
        # ---------------------------------------------

        audit_record = create_audit_record(
            emission_record,
            source_document=source_document,
        )

        results.append(audit_record)

    return results