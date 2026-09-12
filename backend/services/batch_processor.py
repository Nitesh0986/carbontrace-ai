"""
CarbonTrace AI
Batch Emission Processor

Connects activity-data ingestion with the
emission calculation pipeline.
"""

from backend.services.emission_pipeline import process_emission
from backend.services.audit_logger import create_audit_record


def process_activity_records(records: list) -> list:
    """
    Process multiple ActivityRecord objects.

    Each activity is sent through the emission pipeline
    and an audit record is created.
    """

    results = []

    for record in records:

        emission_record = process_emission(
            activity=record.activity,
            quantity=record.quantity,
            unit=record.unit,
            context=record.context,
        )

        audit_record = create_audit_record(emission_record)

        results.append(audit_record)

    return results