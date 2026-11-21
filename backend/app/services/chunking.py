
import tiktoken

TOKENIZER = tiktoken.get_encoding("cl100k_base")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 75


def chunk_pages(
    pages: list[dict],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[dict]:
    """
    Split extracted PDF pages into overlapping text chunks.

    Each chunk retains its original page number.
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be non-negative and smaller than chunk size."
        )

    chunks = []
    chunk_index = 0

    for page in pages:
        text = page["text"].strip()

        if not text:
            continue

        tokens = TOKENIZER.encode(text)
        start = 0

        while start < len(tokens):
            end = min(start + chunk_size, len(tokens))

            chunk_text = TOKENIZER.decode(tokens[start:end]).strip()

            if chunk_text:
                chunks.append(
                    {
                        "chunk_index": chunk_index,
                        "page_number": page["page_number"],
                        "content": chunk_text,
                        "token_count": end - start,
                    }
                )
                chunk_index += 1

            if end == len(tokens):
                break

            start = end - chunk_overlap

    return chunks