
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL,
    storage_path TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    document_id UUID NOT NULL
        REFERENCES documents(id)
        ON DELETE CASCADE,

    content TEXT NOT NULL,
    embedding VECTOR(384),
    page_number INTEGER,
    chunk_index INTEGER NOT NULL,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE (document_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx
ON document_chunks
USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS document_chunks_document_id_idx
ON document_chunks(document_id);
