import os
import shutil

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.database.models import User
from backend.auth.dependencies import get_current_user
from backend.schemas.document_schema import DocumentResponse
from backend.services.document_service import (
    save_document, get_corpus_documents, get_document_by_id, delete_document
)
from backend.services.corpus_service import get_owned_corpus_or_404

router = APIRouter(
    prefix="/corpora/{corpus_id}/documents",
    tags=["Documents"]
)

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx", ".md", ".markdown"}

@router.post("/upload", response_model=DocumentResponse)
def upload_document(corpus_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_owned_corpus_or_404(db, corpus_id, current_user.id)

    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{extension}'. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    file_path = f"uploads/{corpus_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = save_document(db=db, filename=file.filename, filepath=file_path, corpus_id=corpus_id)

    return document


@router.get("", response_model=list[DocumentResponse])
def list_documents(corpus_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_owned_corpus_or_404(db, corpus_id, current_user.id)
    return get_corpus_documents(db, corpus_id)


@router.delete("/{document_id}")
def remove_document(corpus_id: int, document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_owned_corpus_or_404(db, corpus_id, current_user.id)

    document = get_document_by_id(db, document_id)
    if not document or document.corpus_id != corpus_id:
        raise HTTPException(status_code=404, detail="Document not found")

    delete_document(db, document)
    return {"message": "Document deleted successfully"}