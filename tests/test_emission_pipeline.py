"""
CarbonTrace AI
Emission Calculation Pipeline

Pipeline:

1. Scope classification
2. Emission-factor matching
3. Deterministic emission calculation
4. Factor provenance preservation
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
    Process one emission activity.

    LLMs are not responsible for:
    - emission factors
    - arithmetic
    - final CO2e calculation

    Those operations are deterministic.
    """

    scope = classify_scope(
        activity,
        context
    )

    factor_data = find_emission_factor(
        activity,
        unit
    )

    emissions = calculate_emissions(
        quantity,
        factor_data["emission_factor"]
    )

    return {

        "activity":
            activity,

        "quantity":
            quantity,

        "unit":
            unit,

        "context":
            context,

        "scope":
            scope,

        "emission_factor":
            factor_data[
                "emission_factor"
            ],

        "factor_unit":
            factor_data[
                "factor_unit"
            ],

        # -----------------------------------------
        # Factor provenance
        # -----------------------------------------

        "factor_source":
            factor_data[
                "source"
            ],

        "factor_year":
            factor_data[
                "source_year"
            ],

        "factor_methodology":
            factor_data[
                "methodology"
            ],

        "factor_region":
            factor_data[
                "region"
            ],

        "factor_status":
            factor_data[
                "status"
            ],

        "emissions_kg_co2e":
            emissions,
    }