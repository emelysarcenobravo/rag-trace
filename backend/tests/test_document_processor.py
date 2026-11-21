
import fitz
import pytest

from app.services.document_processor import (
    PDFProcessingError,
    extract_pages,
)


def create_test_pdf():
    """Create a small PDF for testing."""
    pdf = fitz.open()
    page = pdf.new_page()
    page.insert_text((72, 72), "RagTrace PDF extraction test.")

    pdf_bytes = pdf.tobytes()
    pdf.close()

    return pdf_bytes


def test_extract_pages():
    pdf_bytes = create_test_pdf()

    pages = extract_pages(pdf_bytes)

    assert len(pages) == 1
    assert pages[0]["page_number"] == 1
    assert "RagTrace PDF extraction test." in pages[0]["text"]


def test_empty_pdf():
    with pytest.raises(PDFProcessingError):
        extract_pages(b"")


def test_invalid_pdf():
    with pytest.raises(PDFProcessingError):
        extract_pages(b"This is not a PDF.")