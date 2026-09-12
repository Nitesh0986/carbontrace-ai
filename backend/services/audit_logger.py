"""
CarbonTrace AI
Advanced Audit Trail Service

Creates a traceable and explainable record
for every emission calculation.
"""

from datetime import datetime, timezone
import uuid


def create_audit_record(
    emission_record: dict,
    source_document: str = "unknown",
) -> dict:
    """
    Create a detailed audit record.

    The audit record stores:
    - Unique record ID
    - Source document
    - Activity data
    - Scope
    - Emission factor
    - Calculation
    - Final result
    - Timestamp
    - Validation status
    """

    quantity = emission_record["quantity"]
    emission_factor = emission_record["emission_factor"]

    emissions = emission_record["emissions_kg_co2e"]

    # Deterministic calculation expression
    calculation = (
        f"{quantity} × {emission_factor}"
    )

    # Independent validation
    expected_emissions = (
        quantity * emission_factor
    )

    validation_passed = (
        abs(expected_emissions - emissions) < 0.000001
    )

    return {
        # ---------------------------------------------
        # Audit identity
        # ---------------------------------------------

        "record_id": str(uuid.uuid4()),

        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        # ---------------------------------------------
        # Source traceability
        # ---------------------------------------------

        "source_document": source_document,

        # ---------------------------------------------
        # Activity information
        # ---------------------------------------------

        "activity": emission_record["activity"],

        "quantity": quantity,

        "unit": emission_record["unit"],

        "context": emission_record["context"],

        # ---------------------------------------------
        # Classification
        # ---------------------------------------------

        "scope": emission_record["scope"],

        # ---------------------------------------------
        # Emission factor
        # ---------------------------------------------

        "emission_factor": emission_factor,

        "factor_unit": emission_record["factor_unit"],

        "factor_source": "CarbonTrace configured factor dataset",

        "factor_version": "demo-v1",

        # ---------------------------------------------
        # Calculation
        # ---------------------------------------------

        "calculation": calculation,

        "emissions_kg_co2e": emissions,

        # ---------------------------------------------
        # Validation
        # ---------------------------------------------

        "validation_status": (
            "PASS"
            if validation_passed
            else "FAIL"
        ),
    }