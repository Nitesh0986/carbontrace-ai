from backend.models.agent_output import (
    ExtractedActivity,
    ExtractedActivities,
)


def test_extracted_activity():

    result = ExtractedActivity(
        activity="diesel",
        quantity=300,
        unit="litre",
        context="company-owned truck",
    )

    assert result.activity == "diesel"
    assert result.quantity == 300
    assert result.unit == "litre"
    assert result.context == "company-owned truck"


def test_multiple_extracted_activities():

    result = ExtractedActivities(
        activities=[
            ExtractedActivity(
                activity="diesel",
                quantity=300,
                unit="litre",
                context="company-owned truck",
            ),
            ExtractedActivity(
                activity="electricity",
                quantity=5000,
                unit="kWh",
                context="purchased electricity from the grid",
            ),
        ]
    )

    assert len(result.activities) == 2

    assert result.activities[0].activity == "diesel"
    assert result.activities[0].quantity == 300

    assert result.activities[1].activity == "electricity"
    assert result.activities[1].quantity == 5000