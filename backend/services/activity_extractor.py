"""
CarbonTrace AI
Activity Extraction Service

Converts raw document text into structured ActivityRecord objects.

Currently this uses simple deterministic demo rules.
Later, the Lyzr agent will perform the actual extraction.
"""

import re

from backend.models.activity import ActivityRecord


def extract_activities(text: str) -> list[ActivityRecord]:
    """
    Extract known emission activities from document text.

    This is a temporary MVP/demo extractor.
    Lyzr will replace this logic later.
    """

    records = []

    # Find diesel quantities
    diesel_matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*litres?\s+of\s+diesel",
        text.lower(),
    )

    for quantity in diesel_matches:
        records.append(
            ActivityRecord(
                activity="diesel",
                quantity=float(quantity),
                unit="litre",
                context="company-owned delivery trucks",
            )
        )

    # Find electricity quantities
    electricity_matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*kwh\s+of\s+electricity",
        text.lower(),
    )

    for quantity in electricity_matches:
        records.append(
            ActivityRecord(
                activity="electricity",
                quantity=float(quantity),
                unit="kWh",
                context="purchased electricity from the grid",
            )
        )

    return records