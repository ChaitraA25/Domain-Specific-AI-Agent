from sqlalchemy.orm import Session

from backend.database.models import ChatHistory


def save_chat(db: Session, user_id: int, corpus_id: int, question: str, answer: str):
    chat = ChatHistory(user_id=user_id, corpus_id=corpus_id, question=question, answer=answer)

    db.add(chat)
    db.commit()
    db.refresh(chat)

    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id, ChatHistory.corpus_id == corpus_id)
        .order_by(ChatHistory.created_at.desc()).all()
    )
    if len(chats) > 10:
        for old_chat in chats[10:]:
            db.delete(old_chat)
        db.commit()

    return chat


def get_chat_history(db: Session, user_id: int, corpus_id: int):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id, ChatHistory.corpus_id == corpus_id)
        .order_by(ChatHistory.created_at.desc()).all()
    )

def get_recent_turns_for_prompt(db: Session, user_id: int, corpus_id: int, limit: int = 5) -> str:
    """
    Builds a short conversational-memory block from the last `limit` turns,
    oldest first, so the LLM can resolve follow-ups like "what about the
    second one?" This was previously missing entirely - chat history was
    saved to the DB but never read back into the prompt.
    """
    history = get_chat_history(db, user_id=user_id, corpus_id=corpus_id)

    recent = history[:limit]  # get_chat_history is already ordered newest-first

    recent = list(reversed(recent))  # flip to oldest-first so it reads in order

    if not recent:
        return ""

    lines = []
    for turn in recent:
        lines.append(f"User: {turn.question}")
        lines.append(f"Assistant: {turn.answer}")

    return "\n".join(lines)