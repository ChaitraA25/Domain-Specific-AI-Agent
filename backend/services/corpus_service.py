from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.database.models import Corpus


def create_corpus(db: Session, name: str, owner_id: int):
    corpus = Corpus(name=name, owner_id=owner_id)
    db.add(corpus)
    db.commit()
    db.refresh(corpus)
    return corpus


def get_user_corpora(db: Session, owner_id: int):
    return (
        db.query(Corpus).filter(Corpus.owner_id == owner_id)
        .order_by(Corpus.created_at.desc()).all()
    )


def get_corpus_by_id(db: Session, corpus_id: int):
    return db.query(Corpus).filter(Corpus.id == corpus_id).first()


def get_owned_corpus_or_404(db: Session, corpus_id: int, user_id: int):
    """Every corpus-scoped route calls this first - it's the single place
    that enforces 'you can only touch your own corpora'."""
    corpus = get_corpus_by_id(db, corpus_id)

    if not corpus:
        raise HTTPException(status_code=404, detail="Corpus not found")

    if corpus.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this corpus")

    return corpus


def delete_corpus(db: Session, corpus: Corpus):
    db.delete(corpus)
    db.commit()