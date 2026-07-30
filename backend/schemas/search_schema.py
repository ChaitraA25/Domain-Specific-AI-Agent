from pydantic import BaseModel

class SearchRequest(BaseModel):
    query : str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]

