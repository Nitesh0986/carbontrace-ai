"""
CarbonTrace AI
PDF Ingestion Service

Extracts raw text from PDF documents.

This service does NOT:
- classify emissions
- choose emission factors
- calculate CO2e

It only extracts document text.
"""

from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from all pages of a PDF.

    Parameters
    ----------
    file_path : str
        Path to the PDF document.

    Returns
    -------
    str
        Combined text extracted from the PDF.
    """

    reader = PdfReader(file_path)

    extracted_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            extracted_text.append(text)

    return "\n".join(extracted_text)