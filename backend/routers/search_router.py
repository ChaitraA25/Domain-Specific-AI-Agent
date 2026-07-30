from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.auth.dependencies import get_current_user

from backend.database.models import User

from backend.schemas.search_schema import SearchRequest,AnswerResponse

from backend.vectorstore.retrieval import retrieve_chunks

from backend.services.llm_service import generate_answer
from backend.services.chat_service import save_chat


router = APIRouter(
    prefix="/ask",
    tags=["Ask"]
)

@router.post("",response_model=AnswerResponse)
def ask_question(request: SearchRequest,db:Session= Depends(get_db),current_user:User = Depends(get_current_user)):
    
    results=retrieve_chunks(request.query)

    chunks = results["documents"][0]

    metadatas = results["metadatas"][0]

    if not chunks:
        return AnswerResponse(answer = "No relevant information found.", sources=[])
    
    context = "\n\n".join(chunks)

    answer = generate_answer(
        question=request.query,context = context
    )

    if answer.strip() == "No relevant information found.":
        save_chat(db=db, user_id=current_user.id, question=request.query, answer=answer)
        return AnswerResponse(answer=answer, sources=[])
    
    sources = list({metadata["filename"] for metadata in metadatas})

    save_chat(db=db,user_id=current_user.id,question=request.query,answer=answer)

    return AnswerResponse(answer=answer,sources=sources)