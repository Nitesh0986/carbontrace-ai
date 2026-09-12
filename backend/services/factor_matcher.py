"""
CarbonTrace AI
Emission Factor Matcher

This module finds the correct emission factor
from our controlled emission-factor dataset.

The AI should NOT invent emission factors.
It should request a factor from this deterministic service.
"""

import csv
from pathlib import Path


FACTOR_FILE = (
    Path(__file__).resolve().parent.parent / "data" / "emission_factors.csv"
)


def find_emission_factor(activity: str, unit: str) -> dict:
    """
    Find an emission factor using activity and unit.

    Example:

    activity = "diesel"
    unit = "litre"

    Returns:

    {
        "activity": "diesel",
        "unit": "litre",
        "emission_factor": 2.5,
        "factor_unit": "kg CO2e/litre",
        "scope": 1
    }
    """

    activity = activity.strip().lower()
    unit = unit.strip().lower()

    with open(FACTOR_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:

            if (
                row["activity"].strip().lower() == activity
                and row["unit"].strip().lower() == unit
            ):
                return {
                    "activity": row["activity"],
                    "unit": row["unit"],
                    "emission_factor": float(row["emission_factor"]),
                    "factor_unit": row["factor_unit"],
                    "scope": int(row["scope"]),
                }

    raise ValueError(
        f"No emission factor found for activity='{activity}' "
        f"and unit='{unit}'."
    )