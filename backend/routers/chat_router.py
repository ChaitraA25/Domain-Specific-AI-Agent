from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.auth.dependencies import get_current_user
from backend.database.models import User

from backend.schemas.chat_schema import ChatResponse
from backend.services.chat_service import get_chat_history

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.get("/history", response_model=list[ChatResponse])
def chat_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_chat_history(
        db,
        current_user.id
    )