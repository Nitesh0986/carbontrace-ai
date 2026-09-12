"""
CarbonTrace AI
Structured AI Output Models
"""

from pydantic import BaseModel, Field


class ExtractedActivity(BaseModel):
    """
    One emission activity extracted from a document.
    """

    activity: str = Field(
        description="Type of emission activity."
    )

    quantity: float = Field(
        description="Amount of activity."
    )

    unit: str = Field(
        description="Unit of the activity."
    )

    context: str = Field(
        description="Context describing the source, ownership, or purpose."
    )


class ExtractedActivities(BaseModel):
    """
    Collection of emission activities extracted from a document.
    """

    activities: list[ExtractedActivity]