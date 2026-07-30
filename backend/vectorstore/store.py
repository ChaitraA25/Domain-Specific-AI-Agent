from backend.vectorstore.chroma_client import collection
from backend.vectorstore.embeddings import generate_embedding

def store_chunks(document_id: int, filename:str, chunks: list[str]):
    for index, chunk in enumerate(chunks):

        embedding = generate_embedding(chunk)

        collection.add(
            ids=[f"doc_{document_id}_chunk_{index}"],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[
                {
                    "document_id":document_id,
                    "filename":filename,
                    "chunk_index":index
                }
            ]
        )

    print(f"Stored {len(chunks)} chunks in ChromaDB")

def delete_document_chunks(document_id:int):

    collection.delete(where={"document_id":document_id})

    print(f"Deleted vectors for document {document_id}")
