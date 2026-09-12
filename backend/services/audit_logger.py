"""
CarbonTrace AI
Audit Trail Service

Creates a traceable record of every emission calculation.

The purpose is to make each result reproducible and auditable.
"""


def create_audit_record(emission_record: dict) -> dict:
    """
    Create an audit record from a processed emission record.
    """

    quantity = emission_record["quantity"]
    emission_factor = emission_record["emission_factor"]

    calculation = (
        f"{quantity} × {emission_factor}"
    )

    return {
        "activity": emission_record["activity"],
        "quantity": quantity,
        "unit": emission_record["unit"],
        "context": emission_record["context"],
        "scope": emission_record["scope"],
        "emission_factor": emission_factor,
        "factor_unit": emission_record["factor_unit"],
        "calculation": calculation,
        "emissions_kg_co2e": emission_record["emissions_kg_co2e"],
    }