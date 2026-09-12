from backend.services.emission_pipeline import process_emission
from backend.services.audit_logger import create_audit_record


def test_audit_record():

    emission_record = process_emission(
        activity="diesel",
        quantity=300,
        unit="litre",
        context="company-owned truck",
    )

    audit_record = create_audit_record(emission_record)

    assert audit_record["activity"] == "diesel"
    assert audit_record["scope"] == 1
    assert audit_record["emission_factor"] == 2.5
    assert audit_record["calculation"] == "300 × 2.5"
    assert audit_record["emissions_kg_co2e"] == 750