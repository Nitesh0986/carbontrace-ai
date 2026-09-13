"""
CarbonTrace AI
Emission Factor Matcher

Finds the correct emission factor from the
controlled emission-factor dataset.

The AI may extract the activity and unit,
but it must NOT invent emission factors.
"""

import csv
from pathlib import Path


FACTOR_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "emission_factors.csv"
)


def normalize_unit(unit: str) -> str:
    """
    Normalize common unit variations.

    Lyzr may return:
        litre
        litres
        L
        liters
        kWh
        tonne-km
        passenger-km

    The factor registry uses one canonical form.
    """

    unit = unit.strip().lower()

    aliases = {
        "litres": "litre",
        "liters": "litre",
        "l": "litre",

        "kwh": "kWh",

        "tonne kms": "tonne-km",
        "tonne km": "tonne-km",
        "tonne-kms": "tonne-km",

        "passenger kms": "passenger-km",
        "passenger km": "passenger-km",
        "passenger-kms": "passenger-km",
    }

    return aliases.get(unit, unit)


def normalize_activity(activity: str) -> str:
    """
    Normalize activity names.
    """

    activity = activity.strip().lower()

    aliases = {
        "diesel fuel": "diesel",
        "petrol fuel": "petrol",
        "gasoline": "petrol",
        "electricity consumption": "electricity",
        "business travel": "business_travel",
        "business-travel": "business_travel",
    }

    return aliases.get(activity, activity)


def find_emission_factor(
    activity: str,
    unit: str
) -> dict:
    """
    Find an emission factor using normalized
    activity and unit values.
    """

    activity = normalize_activity(
        activity
    )

    unit = normalize_unit(
        unit
    )

    with open(
        FACTOR_FILE,
        mode="r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            registry_activity = normalize_activity(
                row["activity"]
            )

            registry_unit = normalize_unit(
                row["unit"]
            )

            if (
                registry_activity == activity
                and registry_unit == unit
            ):

                return {

                    "activity":
                        row["activity"],

                    "unit":
                        row["unit"],

                    "emission_factor":
                        float(
                            row["emission_factor"]
                        ),

                    "factor_unit":
                        row["factor_unit"],

                    "scope":
                        int(
                            row["scope"]
                        ),

                }

    raise ValueError(
        f"No emission factor found for "
        f"activity='{activity}' "
        f"and unit='{unit}'."
    )