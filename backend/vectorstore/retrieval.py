from backend.vectorstore.chroma_client import collection
from backend.vectorstore.embeddings import generate_embedding

def retrieve_chunks(query: str,n_results: int = 3):

    query_embeddings = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embeddings],
        n_results=n_results,
        include=["documents", "distances","metadatas"]
    )
    print("\nRETRIEVAL RESULTS:")
    print(results)
    
    return results