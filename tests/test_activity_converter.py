from backend.models.agent_output import ExtractedActivity
from backend.services.activity_converter import convert_to_activity_record


def test_activity_conversion():

    extracted = ExtractedActivity(
        activity="electricity",
        quantity=5000,
        unit="kWh",
        context="purchased electricity from the grid",
    )

    record = convert_to_activity_record(extracted)

    assert record.activity == "electricity"
    assert record.quantity == 5000
    assert record.unit == "kWh"
    assert record.context == "purchased electricity from the grid"