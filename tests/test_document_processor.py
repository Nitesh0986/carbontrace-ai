from backend.services.document_processor import process_document


def test_document_processing():

    result = process_document(
        "sample_data/sample_emission_report.pdf"
    )

    assert result["activity_count"] == 2

    records = result["audit_records"]

    assert records[0]["activity"] == "diesel"
    assert records[0]["scope"] == 1
    assert records[0]["emissions_kg_co2e"] == 750

    assert records[1]["activity"] == "electricity"
    assert records[1]["scope"] == 2
    assert records[1]["emissions_kg_co2e"] == 500