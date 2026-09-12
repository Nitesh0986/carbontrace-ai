import re

from backend.services.pdf_ingestion import extract_text_from_pdf


def test_pdf_text_extraction():

    text = extract_text_from_pdf(
        "sample_data/sample_emission_report.pdf"
    )

    # Normalize whitespace because PDFs may contain
    # unexpected line breaks between words.
    normalized_text = re.sub(r"\s+", " ", text).strip()

    assert "300 litres of diesel" in normalized_text
    assert "1000 kWh of electricity" in normalized_text