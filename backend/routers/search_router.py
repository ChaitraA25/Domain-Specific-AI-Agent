from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.auth.dependencies import get_current_user
from backend.database.models import User

from backend.schemas.search_schema import SearchRequest, AnswerResponse

from backend.vectorstore.retrieval import retrieve_chunks
from backend.services.llm_service import generate_answer
from backend.services.chat_service import save_chat
from backend.services.corpus_service import get_owned_corpus_or_404
from backend.services.document_service import get_document_by_id

router = APIRouter(
    prefix="/corpora/{corpus_id}/query",
    tags=["Ask"]
)


@router.post("", response_model=AnswerResponse)
def ask_question(corpus_id: int, request: SearchRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_owned_corpus_or_404(db, corpus_id, current_user.id)

    results = retrieve_chunks(corpus_id, request.query)

    if not results:
        answer = "No relevant information found."
        save_chat(db=db, user_id=current_user.id, corpus_id=corpus_id, question=request.query, answer=answer)
        return AnswerResponse(answer=answer, sources=[])

    context = "\n\n".join(r["chunk_text"] for r in results)
    answer = generate_answer(question=request.query, context=context)

    sources = []
    seen = set()
    for r in results:
        document = get_document_by_id(db, r["document_id"])
        filename = document.filename if document else "unknown"
        label = f"{filename} (page {r['page']})" if r.get("page") else filename
        if label not in seen:
            sources.append(label)
            seen.add(label)

    save_chat(db=db, user_id=current_user.id, corpus_id=corpus_id, question=request.query, answer=answer)

    return AnswerResponse(answer=answer, sources=sources)