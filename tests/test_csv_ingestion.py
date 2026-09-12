from backend.services.csv_ingestion import load_csv


def test_csv_ingestion():

    records = load_csv("sample_data/activities.csv")

    assert len(records) == 4

    assert records[0].activity == "diesel"
    assert records[0].quantity == 300
    assert records[0].unit == "litre"

    assert records[1].activity == "electricity"
    assert records[1].quantity == 1000