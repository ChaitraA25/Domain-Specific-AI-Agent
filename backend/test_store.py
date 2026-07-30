from vectorstore.store import store_chunks
from vectorstore.chroma_client import collection

# chunks = [
#     "Python is a programming language.",
#     "FastAPI is a web framework.",
#     "ChromaDB stores vectors."
# ]

# store_chunks(
#     document_id=1,
#     chunks=chunks
# )

# print(collection.count())

results = collection.get()

print(results["ids"])