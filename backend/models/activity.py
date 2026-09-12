"""
CarbonTrace AI
Activity Data Model

Defines the standard structure used internally
for emission activity data.
"""


class ActivityRecord:
    """
    Represents one normalized emission activity.
    """

    def __init__(
        self,
        activity: str,
        quantity: float,
        unit: str,
        context: str,
    ):
        self.activity = activity
        self.quantity = quantity
        self.unit = unit
        self.context = context

    def to_dict(self) -> dict:
        """
        Convert the activity record into a dictionary.
        """

        return {
            "activity": self.activity,
            "quantity": self.quantity,
            "unit": self.unit,
            "context": self.context,
        }