"""
CarbonTrace AI
Agent Interface

Provides a common interface for AI-based activity extraction.

The default mode remains local/mock until the real Lyzr
integration is configured.
"""

from backend.models.activity import ActivityRecord
from backend.models.agent_output import ExtractedActivity
from backend.services.activity_extractor import extract_activities


def extract_activities_with_agent(
    text: str,
    use_lyzr: bool = False,
) -> list[ActivityRecord]:
    """
    Extract activities using either:

    - Local extractor
    - Lyzr agent

    The result is always converted into ActivityRecord.
    """

    if use_lyzr:
        from agents.lyzr_activity_agent import extract_with_lyzr

        extracted = extract_with_lyzr(text)

    else:
        # Temporary local/mock extraction
        mock_records = extract_activities(text)

        extracted = [
            ExtractedActivity(
                activity=record.activity,
                quantity=record.quantity,
                unit=record.unit,
                context=record.context,
            )
            for record in mock_records
        ]

    return [
        ActivityRecord(
            activity=item.activity,
            quantity=item.quantity,
            unit=item.unit,
            context=item.context,
        )
        for item in extracted
    ]