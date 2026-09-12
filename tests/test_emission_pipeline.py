from backend.services.emission_pipeline import process_emission


def test_diesel_emission_pipeline():

    result = process_emission(
        activity="diesel",
        quantity=300,
        unit="litre",
        context="company-owned truck",
    )

    assert result["scope"] == 1
    assert result["emission_factor"] == 2.5
    assert result["emissions_kg_co2e"] == 750