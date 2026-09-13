"""
CarbonTrace AI
Emission Calculation Pipeline

Pipeline:

1. Classify emission scope
2. Match emission factor
3. Calculate CO2e deterministically
4. Return factor provenance
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

    Parameters
    ----------
    activity : str
        Type of activity.

    quantity : float
        Amount of activity.

    unit : str
        Unit of activity.

    context : str
        Context describing the emission source.

    Returns
    -------
    dict
        Complete emission calculation result.
    """

    # --------------------------------------------------
    # STEP 1: CLASSIFY SCOPE
    # --------------------------------------------------

    scope = classify_scope(
        activity,
        context,
    )

    # --------------------------------------------------
    # STEP 2: FIND EMISSION FACTOR
    # --------------------------------------------------

    factor_data = find_emission_factor(
        activity,
        unit,
    )

    # --------------------------------------------------
    # STEP 3: CALCULATE CO2e
    # --------------------------------------------------

    emissions = calculate_emissions(
        quantity,
        factor_data["emission_factor"],
    )

    # --------------------------------------------------
    # STEP 4: RETURN COMPLETE RESULT
    # --------------------------------------------------

    return {
        "activity": activity,

        "quantity": quantity,

        "unit": unit,

        "context": context,

        "scope": scope,

        "emission_factor": factor_data[
            "emission_factor"
        ],

        "factor_unit": factor_data[
            "factor_unit"
        ],

        "emissions_kg_co2e": emissions,

        # Factor provenance
        "factor_source": factor_data.get(
            "factor_source",
            "Unknown",
        ),

        "factor_year": factor_data.get(
            "factor_year",
            "",
        ),

        "factor_methodology": factor_data.get(
            "factor_methodology",
            "",
        ),

        "factor_region": factor_data.get(
            "factor_region",
            "",
        ),

        "factor_status": factor_data.get(
            "factor_status",
            "UNKNOWN",
        ),
    }