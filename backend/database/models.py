from sqlalchemy.orm import mapped_column,Mapped,relationship
from backend.database.db import Base

from datetime import datetime,timezone

from sqlalchemy import ForeignKey


#Represents DB structure
class User(Base):
    __tablename__= "users"

    id:Mapped[int]= mapped_column(primary_key=True,index=True)

    username:Mapped[str] = mapped_column(unique=True,nullable=False)

    email:Mapped[str] = mapped_column(unique=True,nullable=False)

    hashed_password:Mapped[str] = mapped_column(nullable=False)

    role:Mapped[str] = mapped_column(default="user")   # NO longer used

    corpora = relationship("Corpus", back_populates="owner", cascade="all,delete-orphan")

    chats = relationship("ChatHistory",backref="user")

class Corpus(Base):
    """
    A named collection of documents owned by one user
    (e.g. "Client A", "Thesis Lit Review"). This is new -
    it's what lets a user manage multiple separate knowledge bases
    instead of one shared global document pool.
    """
    __tablename__ = "corpora"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner = relationship("User", back_populates="corpora")

    documents = relationship("Document", back_populates="corpus", cascade="all,delete-orphan")

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    filename: Mapped[str] = mapped_column(nullable=False)

    filepath: Mapped[str] = mapped_column(nullable=False)

    uploaded_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    corpus_id: Mapped[int] = mapped_column(ForeignKey("corpora.id"))  # replaces owner_id - documents belong to a corpus, not directly to a user

    corpus = relationship("Corpus", back_populates="documents")


class ChatHistory(Base):
    __tablename__= "chat_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    question:Mapped[str] = mapped_column(nullable=False)

    answer:Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    corpus_id: Mapped[int] = mapped_column(ForeignKey("corpora.id"))  # new -> history is now scoped per-corpus, not just per-user




