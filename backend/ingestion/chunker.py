import re

def split_into_sentences(text: str):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150):
    text = text.strip()
    if not text:
        return []

    sentences = split_into_sentences(text)
    if not sentences:
        return []

    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= chunk_size:
            current = f"{current} {sentence}".strip()
        else:
            if current:
                chunks.append(current)
            overlap_text = current[-overlap:] if current and overlap > 0 else ""
            current = f"{overlap_text} {sentence}".strip()

    if current:
        chunks.append(current)

    print(f"Created {len(chunks)} chunks")

    return chunks