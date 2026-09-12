"""
CarbonTrace AI
CSV Ingestion Service

Reads emission activity data from CSV files
and converts each row into an ActivityRecord.
"""

import csv

from backend.models.activity import ActivityRecord


def load_csv(file_path: str) -> list[ActivityRecord]:
    """
    Load activity records from a CSV file.

    Required columns:
        activity
        quantity
        unit
        context
    """

    records = []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "activity",
            "quantity",
            "unit",
            "context",
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                "CSV must contain: activity, quantity, unit, context"
            )

        for row in reader:

            record = ActivityRecord(
                activity=row["activity"],
                quantity=float(row["quantity"]),
                unit=row["unit"],
                context=row["context"],
            )

            records.append(record)

    return records