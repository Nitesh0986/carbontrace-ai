import pytest

from backend.services.csv_ingestion import load_csv
from backend.services.batch_processor import process_activity_records


def test_batch_processing():

    records = load_csv(
        "sample_data/activities.csv"
    )

    results = process_activity_records(
        records
    )

    assert len(results) == 4

    assert results[0]["activity"] == "diesel"
    assert results[0]["scope"] == 1
    assert results[0]["emissions_kg_co2e"] == pytest.approx(
        798.465
    )

    assert results[1]["activity"] == "electricity"
    assert results[1]["scope"] == 2
    assert results[1]["emissions_kg_co2e"] == pytest.approx(
        130.96
    )

    assert results[2]["activity"] == "freight"
    assert results[2]["scope"] == 3
    assert results[2]["emissions_kg_co2e"] == 500

    assert results[3]["activity"] == "business_travel"
    assert results[3]["scope"] == 3
    assert results[3]["emissions_kg_co2e"] == 300