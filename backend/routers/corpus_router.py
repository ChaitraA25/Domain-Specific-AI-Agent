from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.auth.dependencies import get_current_user
from backend.database.models import User

from backend.schemas.corpus_schema import CorpusCreate, CorpusResponse
from backend.services.corpus_service import (
    create_corpus, get_user_corpora, get_owned_corpus_or_404, delete_corpus
)

router = APIRouter(
    prefix="/corpora",
    tags=["Corpora"]
)


@router.post("", response_model=CorpusResponse)
def create_new_corpus(request: CorpusCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_corpus(db=db, name=request.name, owner_id=current_user.id)


@router.get("", response_model=list[CorpusResponse])
def list_my_corpora(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_corpora(db, current_user.id)


@router.delete("/{corpus_id}")
def remove_corpus(corpus_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    corpus = get_owned_corpus_or_404(db, corpus_id, current_user.id)
    delete_corpus(db, corpus)
    return {"message": "Corpus deleted successfully"}