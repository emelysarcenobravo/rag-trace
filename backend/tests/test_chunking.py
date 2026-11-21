
import pytest

from app.services.chunking import chunk_pages


def test_chunk_pages_returns_content():
    pages = [
        {
            "page_number": 1,
            "text": "RagTrace is an AI-powered document research assistant.",
        }
    ]

    chunks = chunk_pages(pages)

    assert len(chunks) == 1
    assert chunks[0]["page_number"] == 1
    assert chunks[0]["chunk_index"] == 0
    assert "RagTrace" in chunks[0]["content"]


def test_chunk_pages_preserves_page_numbers():
    pages = [
        {"page_number": 1, "text": "First page content."},
        {"page_number": 2, "text": "Second page content."},
    ]

    chunks = chunk_pages(pages)

    assert chunks[0]["page_number"] == 1
    assert chunks[1]["page_number"] == 2


def test_chunk_pages_handles_empty_pages():
    pages = [
        {"page_number": 1, "text": ""},
        {"page_number": 2, "text": "   "},
    ]

    assert chunk_pages(pages) == []


def test_chunk_pages_rejects_invalid_chunk_size():
    with pytest.raises(ValueError):
        chunk_pages([], chunk_size=0)


def test_chunk_pages_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_pages([], chunk_size=100, chunk_overlap=100)