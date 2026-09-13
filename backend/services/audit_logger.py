"""
CarbonTrace AI
Audit Logger

Creates an audit-ready record for every
deterministic emission calculation.
"""

from datetime import datetime, timezone
import uuid


def create_audit_record(
    emission_record: dict,
    source_document: str = "unknown",
) -> dict:
    """
    Create an audit-ready record from an emission calculation.
    """

    quantity = emission_record.get("quantity", 0)
    factor = emission_record.get("emission_factor", 0)
    emissions = emission_record.get("emissions_kg_co2e", 0)

    unit = emission_record.get("unit", "")
    factor_unit = emission_record.get("factor_unit", "")

    # Avoid floating-point artifacts in audit/display values.
    rounded_emissions = round(emissions, 3)

    return {
        "record_id": str(uuid.uuid4()),

        "timestamp": datetime.now(timezone.utc).isoformat(),

        "source_document": source_document,

        "activity": emission_record.get("activity"),

        "quantity": quantity,

        "unit": unit,

        "context": emission_record.get("context"),

        "scope": emission_record.get("scope"),

        "emission_factor": factor,

        "factor_unit": factor_unit,

        "factor_source": emission_record.get(
            "factor_source",
            "Unknown",
        ),

        "factor_year": emission_record.get(
            "factor_year",
            "",
        ),

        "factor_methodology": emission_record.get(
            "factor_methodology",
            "",
        ),

        "factor_region": emission_record.get(
            "factor_region",
            "",
        ),

        "factor_status": emission_record.get(
            "factor_status",
            "UNKNOWN",
        ),

        "calculation": (
            f"{quantity:g} {unit} × "
            f"{factor:g} {factor_unit} = "
            f"{rounded_emissions:.3f} kg CO2e"
        ),

        "emissions_kg_co2e": emissions,

        "validation_status": "PASS",
    }