"""
CarbonTrace AI
Emission Calculation Pipeline

Combines:
1. Scope classification
2. Emission-factor matching
3. Deterministic emission calculation

The individual services remain responsible for their
own logic. This module simply orchestrates them.
"""

from backend.services.scope_classifier import classify_scope
from backend.services.factor_matcher import find_emission_factor
from backend.services.emission_calculator import calculate_emissions


def process_emission(
    activity: str,
    quantity: float,
    unit: str,
    context: str,
) -> dict:
    """
    Process an emission activity from start to finish.

    Returns a complete emission record.
    """

    # Step 1: Determine emission scope
    scope = classify_scope(activity, context)

    # Step 2: Find the appropriate emission factor
    factor_data = find_emission_factor(activity, unit)

    # Step 3: Calculate emissions deterministically
    emissions = calculate_emissions(
        quantity,
        factor_data["emission_factor"],
    )

    # Step 4: Combine everything into one record
    return {
        "activity": activity,
        "quantity": quantity,
        "unit": unit,
        "context": context,
        "scope": scope,
        "emission_factor": factor_data["emission_factor"],
        "factor_unit": factor_data["factor_unit"],
        "emissions_kg_co2e": emissions,
    }