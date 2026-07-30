from pydantic import BaseModel
from datetime import datetime


class ChatResponse(BaseModel):
    question: str
    answer: str
    created_at: datetime

    class Config:
        from_attributes = True

        