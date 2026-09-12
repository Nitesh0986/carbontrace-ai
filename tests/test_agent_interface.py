from backend.services.agent_interface import extract_activities_with_agent


def test_agent_interface():

    text = """
    The company consumed 300 litres of diesel
    for its company-owned delivery trucks.
    """

    records = extract_activities_with_agent(text)

    assert len(records) == 1
    assert records[0].activity == "diesel"
    assert records[0].quantity == 300
    assert records[0].unit == "litre"