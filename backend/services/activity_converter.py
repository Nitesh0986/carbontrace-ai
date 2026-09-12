"""
CarbonTrace AI
Activity Converter

Converts structured AI output into the internal
ActivityRecord used by the deterministic pipeline.
"""

from backend.models.activity import ActivityRecord
from backend.models.agent_output import ExtractedActivity


def convert_to_activity_record(
    extracted: ExtractedActivity,
) -> ActivityRecord:
    """
    Convert AI-extracted activity data into
    an ActivityRecord.
    """

    return ActivityRecord(
        activity=extracted.activity,
        quantity=extracted.quantity,
        unit=extracted.unit,
        context=extracted.context,
    )