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

    role:Mapped[str] = mapped_column(default="user")

    documents = relationship("Document",back_populates="owner",cascade="all,delete-orphan")

    chats = relationship("ChatHistory",backref="user")


class Document(Base):
    __tablename__= "documents"

    id: Mapped[int] = mapped_column(primary_key=True,index=True)

    filename: Mapped[str] = mapped_column(nullable=False)

    filepath: Mapped[str] = mapped_column(nullable=False)

    uploaded_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner = relationship("User",back_populates="documents")


class ChatHistory(Base):
    __tablename__= "chat_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    question:Mapped[str] = mapped_column(nullable=False)

    answer:Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))




