"""
CarbonTrace AI
Lyzr Activity Extraction Agent

Lyzr is responsible for extracting structured
activity data from unstructured ESG documents.

Important:

Lyzr does NOT:
- calculate emissions
- choose emission factors
- determine final CO2e
- perform arithmetic
"""

import os

from lyzr import Studio

from backend.models.agent_output import (
    ExtractedActivities,
)


def create_lyzr_agent():
    """
    Create the CarbonTrace AI Lyzr agent.
    """

    api_key = os.getenv("LYZR_API_KEY")

    if not api_key:
        raise ValueError(
            "LYZR_API_KEY environment variable "
            "is not set."
        )

    studio = Studio(
        api_key=api_key
    )

    agent = studio.create_agent(

        name=
            "CarbonTrace Activity Extraction Agent",

        provider=
            "gpt-4o",

        role=
            "ESG emissions data extraction specialist",

        goal=(
            "Extract emission-related activity data "
            "from ESG and business documents into "
            "structured data."
        ),

        instructions="""

You are an ESG carbon-accounting data extraction agent.

Your job is ONLY to understand the provided document
and extract emission-related activity data.

For every emission activity, extract:

1. activity
2. quantity
3. unit
4. context

IMPORTANT RULES:

- Do NOT calculate CO2e.
- Do NOT multiply quantities.
- Do NOT invent emission factors.
- Do NOT invent quantities.
- Do NOT guess missing information.
- Do NOT change the meaning of the source document.
- Only extract information explicitly supported by the document.
- Preserve useful context such as ownership,
  purchased energy, transportation, or business travel.
- If no emission-related activity is found,
  return an empty activities list.

Examples:

diesel
petrol
electricity
freight
business_travel

Return only structured data.

""",

        response_model=
            ExtractedActivities,
    )

    return agent


def extract_with_lyzr(
    text: str
) -> list:
    """
    Extract emission activities using Lyzr.
    """

    agent = create_lyzr_agent()

    result = agent.run(

        f"""
Extract every emission-related activity
from the following ESG document.

DOCUMENT:

{text}
"""
    )

    # Lyzr returns the Pydantic model directly
    # when response_model is configured.
    return result.activities