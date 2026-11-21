
from pathlib import Path
from typing import Annotated
from uuid import uuid4

import psycopg
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.db.database import get_connection
from app.services.document_processor import (
    PDFProcessingError,
    extract_pages,
)

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024

UPLOAD_DIRECTORY = Path(__file__).resolve().parents[3] / "uploads"


@router.post("/upload", status_code=201)
async def upload_document(
    file: Annotated[UploadFile, File()]
):
    """
    Upload a PDF, extract its text, and save its metadata.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    pdf_bytes = await file.read(MAX_FILE_SIZE + 1)

    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="PDF exceeds the 10 MB file size limit.",
        )

    if not pdf_bytes.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file.",
        )

    try:
        pages = extract_pages(pdf_bytes)
    except PDFProcessingError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    document_id = uuid4()
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

    document_path = UPLOAD_DIRECTORY / f"{document_id}.pdf"
    storage_path = f"uploads/{document_id}.pdf"

    document_path.write_bytes(pdf_bytes)

    try:
        with get_connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents (
                    id,
                    filename,
                    file_type,
                    storage_path
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    document_id,
                    file.filename,
                    "application/pdf",
                    storage_path,
                ),
            )

    except psycopg.Error:
        document_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=503,
            detail="Unable to save document metadata.",
        ) from None

    extracted_characters = sum(
        len(page["text"]) for page in pages
    )

    return {
        "message": "Document uploaded successfully.",
        "document_id": str(document_id),
        "filename": file.filename,
        "page_count": len(pages),
        "extracted_characters": extracted_characters,
        "status": "uploaded",
    }