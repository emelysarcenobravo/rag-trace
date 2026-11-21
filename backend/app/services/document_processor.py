
import fitz


class PDFProcessingError(ValueError):
    """Raised when a PDF cannot be processed."""


def extract_pages(pdf_bytes: bytes) -> list[dict]:
    """
    Extract text from each page of a PDF.

    Returns a list containing each page number and its extracted text.
    """
    if not pdf_bytes:
        raise PDFProcessingError("The uploaded PDF is empty.")

    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
            if pdf.is_encrypted:
                raise PDFProcessingError(
                    "Password-protected PDFs are not supported."
                )

            pages = [
                {
                    "page_number": page_number,
                    "text": page.get_text("text").strip(),
                }
                for page_number, page in enumerate(pdf, start=1)
            ]

    except (fitz.FileDataError, RuntimeError) as error:
        raise PDFProcessingError("Unable to read the PDF file.") from error

    if not any(page["text"] for page in pages):
        raise PDFProcessingError(
            "No extractable text found in the PDF."
        )

    return pages
