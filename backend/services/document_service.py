import os

from sqlalchemy.orm import Session

from backend.database.models import Document

from backend.ingestion.extractor import extract_text
from backend.ingestion.chunker import chunk_text

from backend.vectorstore.store import store_chunks, delete_document_chunks


def save_document(db: Session, filename: str, filepath: str, corpus_id: int):

    document = Document(
        filename=filename,
        filepath=filepath,
        corpus_id=corpus_id
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    try:
        pages = extract_text(filepath)  # list of (page_number, text)

        all_chunks = []
        all_pages = []

        for page_number, page_text in pages:
            page_chunks = chunk_text(page_text)
            all_chunks.extend(page_chunks)
            all_pages.extend([page_number] * len(page_chunks))

        store_chunks(
            corpus_id=corpus_id,
            document_id=document.id,
            chunks=all_chunks,
            pages=all_pages
        )

        print(f"\nCreated {len(all_chunks)} chunks across {len(pages)} page-units")

        for i, chunk in enumerate(all_chunks[:3]):
            print(f"\nChunk {i+1} (page {all_pages[i]})")
            print(f"Length: {len(chunk)}")
            print(chunk[:200])

    except Exception as e:
        print(f"Extraction failed: {e}")

    return document


def get_corpus_documents(db: Session, corpus_id: int):
    return (
        db.query(Document).filter(Document.corpus_id == corpus_id).all()
    )


def get_document_by_id(db: Session, document_id: int):
    return (
        db.query(Document).filter(Document.id == document_id).first()
    )


def delete_document(db: Session, document: Document):
    delete_document_chunks(document.id)

    if os.path.exists(document.filepath):
        os.remove(document.filepath)

    db.delete(document)
    db.commit()