from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.auth.dependencies import get_current_user
from backend.database.models import User

from backend.schemas.chat_schema import ChatResponse
from backend.services.chat_service import get_chat_history
from backend.services.corpus_service import get_owned_corpus_or_404

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.get("/history", response_model=list[ChatResponse])
def chat_history(corpus_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_owned_corpus_or_404(db, corpus_id, current_user.id)
    return get_chat_history(db, corpus_id=corpus_id, user_id=current_user.id)