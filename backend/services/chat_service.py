from sqlalchemy.orm import Session

from backend.database.models import ChatHistory

def save_chat(db: Session,user_id: int,question: str,answer:str):

    chat = ChatHistory(user_id=user_id,question=question,answer=answer)

    db.add(chat)
    db.commit()
    db.refresh(chat)

    chats= ( db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.created_at.desc()).all())
    if len(chats) >10:
        chats_to_delete = chats[10:]

        for old_chat in chats_to_delete:
            db.delete(old_chat)

        db.commit()

    return chat

def get_chat_history(db: Session,user_id: int):

    return (db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.created_at.desc()).all())




