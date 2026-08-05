import numpy as np

from backend.vectorstore.supabase_client import get_connection
from backend.vectorstore.embeddings import generate_embedding


def retrieve_chunks(corpus_id: int, query: str, n_results: int = 4):
    """
    Embeds the query and finds the n_results closest chunks *within this
    corpus only*. The corpus_id filter is what keeps corpora isolated from
    each other - this replaces what a separate ChromaDB collection used to do.
    """
    query_embedding = generate_embedding(query)

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT chunk_text, page, document_id,
                       embedding <=> %s AS distance
                FROM embeddings
                WHERE corpus_id = %s
                ORDER BY distance ASC
                LIMIT %s
                """,
                (np.array(query_embedding), corpus_id, n_results),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    return [
        {"chunk_text": row[0], "page": row[1], "document_id": row[2], "distance": row[3]}
        for row in rows
    ]