"""
CarbonTrace AI
Deterministic Emission Calculation Engine

This module performs carbon emission calculations.

Core formula:

CO2e = Activity Data × Emission Factor

Important:
LLMs should NOT perform the final arithmetic.
The calculation is handled deterministically by Python.
"""


def calculate_emissions(quantity: float, emission_factor: float) -> float:
    """
    Calculate CO2e emissions.

    Parameters
    ----------
    quantity : float
        Amount of activity consumed.
        Example: 300 litres of diesel.

    emission_factor : float
        Emission factor corresponding to the activity unit.
        Example: 2.5 kg CO2e per litre.

    Returns
    -------
    float
        Calculated emissions in kg CO2e.

    Example
    -------
    300 litres × 2.5 kg CO2e/litre
    = 750 kg CO2e
    """

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    if emission_factor < 0:
        raise ValueError("Emission factor cannot be negative.")

    return quantity * emission_factor