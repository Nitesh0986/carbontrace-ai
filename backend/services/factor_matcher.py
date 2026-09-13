"""
CarbonTrace AI
Emission Factor Matcher

Finds emission factors from the controlled
CarbonTrace emission-factor dataset.

The AI must NOT invent emission factors.
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
    """

    value = unit.strip().lower()

    unit_map = {
        "litre": "litre",
        "litres": "litre",
        "liter": "litre",
        "liters": "litre",
        "l": "litre",

        "kwh": "kWh",

        "tonne-km": "tonne-km",
        "tonne km": "tonne-km",
        "tonnekm": "tonne-km",

        "passenger-km": "passenger-km",
        "passenger km": "passenger-km",
        "passengerkm": "passenger-km",
    }

    return unit_map.get(value, unit)


def find_emission_factor(
    activity: str,
    unit: str,
) -> dict:
    """
    Find an emission factor using activity and unit.
    """

    activity = activity.strip().lower()
    unit = normalize_unit(unit)

    if not FACTOR_FILE.exists():
        raise FileNotFoundError(
            f"Emission factor file not found: {FACTOR_FILE}"
        )

    with open(
        FACTOR_FILE,
        mode="r",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            row_activity = (
                row["activity"]
                .strip()
                .lower()
            )

            row_unit = normalize_unit(
                row["unit"]
            )

            if (
                row_activity == activity
                and row_unit == unit
            ):

                return {
                    "activity": row["activity"],

                    "unit": row["unit"],

                    "emission_factor": float(
                        row["emission_factor"]
                    ),

                    "factor_unit": row[
                        "factor_unit"
                    ],

                    "scope": int(
                        row["scope"]
                    ),

                    "factor_source": row.get(
                        "factor_source",
                        "Unknown",
                    ),

                    "factor_year": row.get(
                        "factor_year",
                        "",
                    ),

                    "factor_methodology": row.get(
                        "factor_methodology",
                        "",
                    ),

                    "factor_region": row.get(
                        "factor_region",
                        "",
                    ),

                    "factor_status": row.get(
                        "factor_status",
                        "UNKNOWN",
                    ),
                }

    raise ValueError(
        f"No emission factor found for "
        f"activity='{activity}' "
        f"and unit='{unit}'."
    )