"""
CarbonTrace AI
Scope Classification Service

This module classifies emission activities into
Scope 1, Scope 2, or Scope 3.

The classification is deterministic.
AI may extract the activity/context from documents,
but this service applies the business rules.
"""


def classify_scope(activity: str, context: str) -> int:
    """
    Classify an activity into Scope 1, 2, or 3.

    Parameters
    ----------
    activity : str
        Type of activity.

    context : str
        Information about ownership/control or source.

    Returns
    -------
    int
        Emission scope: 1, 2, or 3.
    """

    activity = activity.strip().lower()
    context = context.strip().lower()

    # Scope 2: purchased electricity
    if activity == "electricity":
        return 2

    # Scope 3: business travel
    if activity == "business_travel":
        return 3

    # Scope 3: third-party logistics / transportation
    if activity == "freight":
        return 3

    # Scope 1: fuel used in company-owned or controlled sources
    fuel_activities = {"diesel", "petrol"}

    if activity in fuel_activities:
        if (
            "company-owned" in context
            or "company owned" in context
            or "owned" in context
            or "controlled" in context
        ):
            return 1

        # If the fuel source belongs to a third party,
        # classify it as Scope 3.
        if (
            "third-party" in context
            or "third party" in context
            or "external" in context
        ):
            return 3

    raise ValueError(
        f"Unable to classify activity='{activity}' "
        f"with context='{context}'."
    )