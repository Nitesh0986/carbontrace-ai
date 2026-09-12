"""
CarbonTrace AI
Lyzr Activity Extraction Agent

Uses Lyzr to extract structured emission activities
from unstructured ESG document text.

The Lyzr agent is responsible only for understanding
and extracting information.

It does NOT:
- calculate CO2e
- select emission factors
- perform final calculations
"""

import os

from lyzr import Studio

from backend.models.agent_output import ExtractedActivities


def create_lyzr_agent():
    """
    Create the Lyzr activity extraction agent.
    """

    api_key = os.getenv("LYZR_API_KEY")

    if not api_key:
        raise ValueError(
            "LYZR_API_KEY environment variable is not set."
        )

    studio = Studio(api_key=api_key)

    agent = studio.create_agent(
        name="CarbonTrace Activity Extraction Agent",
        provider="gpt-4o",
        role="ESG emissions data extraction specialist",
        goal=(
            "Extract emission-related activities from ESG "
            "documents into structured data."
        ),
        instructions="""
You are an ESG carbon-accounting data extraction agent.

Read the provided document carefully.

Identify every emission-related activity.

For each activity extract:

- activity
- quantity
- unit
- context

Rules:

1. Do not calculate CO2e.
2. Do not invent emission factors.
3. Do not guess missing quantities.
4. Preserve the original meaning of the document.
5. Return only information supported by the document.
6. If no emission activity is found, return an empty activities list.
""",
    )

    return agent


def extract_with_lyzr(text: str) -> list:
    """
    Extract all emission activities from document text
    using the Lyzr agent.
    """

    agent = create_lyzr_agent()

    result = agent.run(
        f"""
Extract every emission-related activity from this ESG document.

DOCUMENT:
{text}
""",
        response_format=ExtractedActivities,
    )

    return result.activities