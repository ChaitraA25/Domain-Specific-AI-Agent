import os
import shutil

from fastapi import APIRouter,Depends,File,UploadFile,HTTPException

from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.database.models import User
from backend.auth.dependencies import get_current_user
from backend.schemas.document_schema import DocumentResponse
from backend.services.document_service import save_document, get_user_documents, get_document_by_id,delete_document,get_all_documents

router=APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload",response_model=DocumentResponse)
def upload_document(file:UploadFile=File(...),db:Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    file_path = f"uploads/{file.filename}"
    """
    Saving the file
    """
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    document= save_document(db=db,filename=file.filename,filepath=file_path,owner_id=current_user.id)

    return document

@router.get("",response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db),current_user: User=Depends(get_current_user)):    
    if current_user.role == "admin":
        return get_all_documents(db)
    return get_user_documents(db, current_user.id)

@router.delete("/{document_id}")
def remove_document(document_id:int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    document = get_document_by_id(db,document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    
    if document.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this document"
        )
    
    delete_document(
        db,
        document
    )

    return {"message" : "Document deleted succcesfully"}






