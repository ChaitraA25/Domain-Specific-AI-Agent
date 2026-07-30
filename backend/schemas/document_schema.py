from datetime import datetime

from pydantic import BaseModel
#Represents API structure

class DocumentResponse(BaseModel):
    id: int
    filename:str
    uploaded_at: datetime

    class Config:
        from_attributes=True
