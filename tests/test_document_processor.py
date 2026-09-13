import pytest

from backend.services.document_processor import process_document


def test_document_processing():

    result = process_document(
        "sample_data/sample_emission_report.pdf"
    )

    assert result["activity_count"] == 2

    records = result["audit_records"]

    # -------------------------------------------------
    # Diesel → Scope 1
    # Official 2026 factor:
    # 2.66155 kg CO2e/litre
    # 300 × 2.66155 = 798.465
    # -------------------------------------------------

    assert records[0]["activity"] == "diesel"
    assert records[0]["scope"] == 1

    assert records[0]["emissions_kg_co2e"] == pytest.approx(
        798.465
    )

    # -------------------------------------------------
    # Electricity → Scope 2
    # Official 2026 factor:
    # 0.13096 kg CO2e/kWh
    # 1000 × 0.13096 = 130.96
    # -------------------------------------------------

    assert records[1]["activity"] == "electricity"
    assert records[1]["scope"] == 2

    assert records[1]["emissions_kg_co2e"] == pytest.approx(
        130.96
    )