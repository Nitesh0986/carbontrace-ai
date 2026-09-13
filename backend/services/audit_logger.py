"""
CarbonTrace AI
Advanced Audit Trail Service

Creates a traceable and explainable record
for every emission calculation.

Each audit record preserves:
- Source document
- Activity data
- Scope
- Emission factor
- Factor provenance
- Calculation
- Final result
- Validation
- Timestamp
"""

from datetime import datetime, timezone
import uuid


def create_audit_record(
    emission_record: dict,
    source_document: str = "unknown",
) -> dict:
    """
    Create a complete audit record for one
    emission calculation.
    """

    quantity = emission_record["quantity"]

    emission_factor = (
        emission_record["emission_factor"]
    )

    emissions = (
        emission_record["emissions_kg_co2e"]
    )

    # ---------------------------------------------
    # Deterministic calculation expression
    # ---------------------------------------------

    calculation = (
        f"{quantity} × {emission_factor}"
    )

    expected_emissions = (
        quantity * emission_factor
    )

    # ---------------------------------------------
    # Calculation validation
    # ---------------------------------------------

    validation_passed = (
        abs(
            expected_emissions - emissions
        ) < 0.000001
    )

    return {

        # -----------------------------------------
        # Audit identity
        # -----------------------------------------

        "record_id":
            str(uuid.uuid4()),

        "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),

        # -----------------------------------------
        # Source document
        # -----------------------------------------

        "source_document":
            source_document,

        # -----------------------------------------
        # Activity data
        # -----------------------------------------

        "activity":
            emission_record["activity"],

        "quantity":
            quantity,

        "unit":
            emission_record["unit"],

        "context":
            emission_record["context"],

        # -----------------------------------------
        # Scope
        # -----------------------------------------

        "scope":
            emission_record["scope"],

        # -----------------------------------------
        # Emission factor
        # -----------------------------------------

        "emission_factor":
            emission_factor,

        "factor_unit":
            emission_record[
                "factor_unit"
            ],

        # -----------------------------------------
        # Factor provenance
        # -----------------------------------------

        "factor_source":
            emission_record.get(
                "factor_source",
                "Unknown"
            ),

        "factor_year":
            emission_record.get(
                "factor_year"
            ),

        "factor_methodology":
            emission_record.get(
                "factor_methodology",
                "Unknown"
            ),

        "factor_region":
            emission_record.get(
                "factor_region",
                "Unknown"
            ),

        "factor_status":
            emission_record.get(
                "factor_status",
                "unknown"
            ),

        # -----------------------------------------
        # Calculation
        # -----------------------------------------

        "calculation":
            calculation,

        "emissions_kg_co2e":
            emissions,

        # -----------------------------------------
        # Validation
        # -----------------------------------------

        "validation_status":
            (
                "PASS"
                if validation_passed
                else "FAIL"
            ),
    }