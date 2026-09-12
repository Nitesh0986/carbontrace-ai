"""
CarbonTrace AI
Agent Interface

Controls whether activity extraction uses:
- Local deterministic extractor
- Lyzr AI agent

The Lyzr agent is responsible only for
understanding unstructured document text.

It does NOT calculate emissions.
"""

import os

from backend.models.activity import ActivityRecord
from backend.models.agent_output import ExtractedActivity
from backend.services.activity_extractor import extract_activities


def extract_activities_with_agent(
    text: str,
    use_lyzr: bool = False,
) -> list[ActivityRecord]:
    """
    Extract emission activities.

    If use_lyzr=True:
        Use the Lyzr AI agent.

    If use_lyzr=False:
        Use the local deterministic extractor.
    """

    # -----------------------------------------
    # Decide whether Lyzr should be used
    # -----------------------------------------

    if use_lyzr:

        from agents.lyzr_activity_agent import (
            extract_with_lyzr
        )

        extracted = extract_with_lyzr(text)

    else:

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


    # -----------------------------------------
    # Convert structured AI output
    # into our internal ActivityRecord model
    # -----------------------------------------

    return [
        ActivityRecord(
            activity=item.activity,
            quantity=item.quantity,
            unit=item.unit,
            context=item.context,
        )
        for item in extracted
    ]


def should_use_lyzr() -> bool:
    """
    Read the Lyzr activation setting
    from the environment.

    .env example:

    CARBONTRACE_USE_LYZR=true
    """

    value = os.getenv(
        "CARBONTRACE_USE_LYZR",
        "false",
    )

    return value.strip().lower() in {
        "true",
        "1",
        "yes",
        "on",
    }