from datetime import datetime
from pydantic import BaseModel


class CorpusCreate(BaseModel):
    name: str


class CorpusResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True