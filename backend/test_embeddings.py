from vectorstore.embeddings import generate_embedding

embedding1 = generate_embedding(
    "Python is a programming language"
)

embedding2 = generate_embedding(
    "Coding with Python"
)

embedding3 = generate_embedding(
    "Pizza is delicious"
)

print(type(embedding1))
print(embedding1[:5])

print(type(embedding2))
print(embedding2[:5])

print(type(embedding3))
print(embedding3[:5])