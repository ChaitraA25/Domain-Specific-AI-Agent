import numpy as np

from backend.vectorstore.supabase_client import get_connection
from backend.vectorstore.embeddings import generate_embedding

# Cosine distance ranges 0 (identical) to 2 (opposite). Chunks with distance
# above this are treated as "not actually relevant" and discarded, even if
# they were the closest thing available - top-k alone doesn't guarantee
# relevance, only relative ranking.
DISTANCE_THRESHOLD = 0.6

def retrieve_chunks(corpus_id: int, query: str, n_results: int = 4):

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

    results = [
        {"chunk_text": row[0], "page": row[1], "document_id": row[2], "distance": row[3]}
        for row in rows
    ]

    # Debug print while calibrating - shows every candidate and whether it
    # survives the cutoff, so you can tune DISTANCE_THRESHOLD against your
    # actual data instead of guessing blindly.
    for r in results:
        kept = "KEPT" if r["distance"] <= DISTANCE_THRESHOLD else "DROPPED"
        print(f"[{kept}] distance={r['distance']:.4f} | {r['chunk_text'][:80]!r}")

    return [r for r in results if r["distance"] <= DISTANCE_THRESHOLD]