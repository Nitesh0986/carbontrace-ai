from backend.services.activity_extractor import extract_activities


def test_extract_diesel():

    text = """
    The company consumed 300 litres of diesel
    for its company-owned delivery trucks.
    """

    records = extract_activities(text)

    assert len(records) == 1
    assert records[0].activity == "diesel"
    assert records[0].quantity == 300
    assert records[0].unit == "litre"


def test_extract_electricity():

    text = """
    The company purchased 5000 kWh of electricity
    from the grid.
    """

    records = extract_activities(text)

    assert len(records) == 1
    assert records[0].activity == "electricity"
    assert records[0].quantity == 5000
    assert records[0].unit == "kWh"