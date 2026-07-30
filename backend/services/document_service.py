# We will do operations like removing file from disk, so import os
import os

from sqlalchemy.orm import Session

from backend.database.models import Document

from backend.ingestion.extractor import extract_text
from backend.ingestion.chunker import chunk_text

from backend.vectorstore.store import store_chunks,delete_document_chunks

from backend.vectorstore.chroma_client import collection


def save_document(db:Session,filename:str,filepath:str,owner_id:int):

    document = Document(
        filename=filename,
        filepath=filepath,
        owner_id=owner_id
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    try:
        extracted_text = extract_text(filepath)

        chunks = chunk_text(extracted_text)

        store_chunks(document_id=document.id,filename=document.filename,chunks=chunks)

        print("Total vectors in ChromaDB:", collection.count())

        print(f"\nCreated {len(chunks)} chunks")

        for i, chunk in enumerate(chunks[:3]):
            print(f"\nChunk {i+1}")
            print(f"Length: {len(chunk)}")
            print(chunk[:200])

    except Exception as e:
        print(f"Extraction failed: {e}")
    
    return document

def get_user_documents(db:Session,owner_id):

    return (
        db.query(Document).filter(Document.owner_id == owner_id).all()
    )

def get_document_by_id(db: Session,document_id: int):
    return (
        db.query(Document).filter(Document.id == document_id).first()
    )

def get_all_documents(db: Session):
    return db.query(Document).all()

def delete_document(db: Session, document: Document):
    # Remove vectors
    delete_document_chunks(document.id)
    
    # Remove physical file   
    if os.path.exists(document.filepath):
        os.remove(document.filepath)

    # Remove DB record
    db.delete(document)
    db.commit()


