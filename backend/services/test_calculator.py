from backend.services.emission_calculator import calculate_emissions


def test_diesel_calculation():
    result = calculate_emissions(300, 2.5)

    assert result == 750