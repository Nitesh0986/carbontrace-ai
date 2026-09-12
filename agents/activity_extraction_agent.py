"""
CarbonTrace AI
Lyzr Activity Extraction Agent

The agent extracts structured emission activity data
from unstructured ESG document text.

AI responsibility:
- Understand document text
- Identify activities
- Extract quantities
- Extract units
- Extract context

AI does NOT:
- Calculate emissions
- Invent emission factors
- Make the final numerical calculation
"""

import os

from lyzr import Studio


LYZR_API_KEY = os.getenv("LYZR_API_KEY")


def create_activity_agent():

    if not LYZR_API_KEY:
        raise ValueError(
            "LYZR_API_KEY environment variable is not set."
        )

    studio = Studio(api_key=LYZR_API_KEY)

    agent = studio.create_agent(
        name="CarbonTrace Activity Extraction Agent",
        provider="gpt-4o",
        role="ESG data extraction specialist",
        goal=(
            "Extract emission activity data from ESG documents "
            "into structured fields."
        ),
        instructions="""
        Read the provided ESG document text carefully.

        Identify emission-related activities.

        For each activity extract:
        - activity
        - quantity
        - unit
        - context

        Do not calculate CO2e.

        Do not invent emission factors.

        Do not assign a final emission value.

        If information is missing or ambiguous, do not guess.
        """,
    )

    return agent