from backend.services.factor_matcher import find_emission_factor


def test_diesel_factor():
    result = find_emission_factor("diesel", "litre")

    assert result["emission_factor"] == 2.5
    assert result["scope"] == 1


def test_electricity_factor():
    result = find_emission_factor("electricity", "kWh")

    assert result["emission_factor"] == 0.5
    assert result["scope"] == 2