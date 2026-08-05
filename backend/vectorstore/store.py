import numpy as np

from backend.vectorstore.supabase_client import get_connection
from backend.vectorstore.embeddings import generate_embedding


def store_chunks(corpus_id: int, document_id: int, chunks: list[str], pages: list[int | None] = None):
    """
    Embeds each chunk and inserts it into the `embeddings` table in Supabase,
    tagged with corpus_id (for isolation between corpora) and document_id
    (so we can delete just this document's vectors later).
    """
    if pages is None:
        pages = [None] * len(chunks)

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for chunk, page in zip(chunks, pages):
                embedding = generate_embedding(chunk)
                cur.execute(
                    """
                    INSERT INTO embeddings (corpus_id, document_id, chunk_text, page, embedding)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (corpus_id, document_id, chunk, page, np.array(embedding)),
                )
        conn.commit()
        print(f"Stored {len(chunks)} chunks in Supabase for document {document_id}")
    finally:
        conn.close()


def delete_document_chunks(document_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM embeddings WHERE document_id = %s", (document_id,))
        conn.commit()
        print(f"Deleted vectors for document {document_id}")
    finally:
        conn.close()