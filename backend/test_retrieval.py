from vectorstore.retrieval import retrieve_chunks

results = retrieve_chunks(
    "What is FastAPI?"
)

documents = results["documents"][0]
distances = results["distances"][0]

for doc, distance in zip(documents, distances):
    print(f"\nDistance: {distance}")
    print(doc)