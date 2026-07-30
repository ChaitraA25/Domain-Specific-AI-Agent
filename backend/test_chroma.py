from vectorstore.chroma_client import collection


# collection.add(
#     ids=["test_2"],
#     documents=["FastAPI is a modern Python framework."]
# )
# print(collection.count())

results = collection.get()

print(results)