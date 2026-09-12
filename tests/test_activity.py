from backend.models.activity import ActivityRecord


def test_activity_record():

    record = ActivityRecord(
        activity="diesel",
        quantity=300,
        unit="litre",
        context="company-owned truck",
    )

    result = record.to_dict()

    assert result["activity"] == "diesel"
    assert result["quantity"] == 300
    assert result["unit"] == "litre"
    assert result["context"] == "company-owned truck"