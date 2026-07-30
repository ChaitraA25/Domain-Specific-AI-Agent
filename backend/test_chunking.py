from ingestion.chunker import chunk_text


text = ( "Python is Awesome" )

chunks=chunk_text(text,10,2)

print(f"Total Chunks: {len(chunks)}")

for index,chunk in enumerate(chunks):
    print(f"\nChunk {index + 1}")
    print(chunk)


# print(chunks[0])