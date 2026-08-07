from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.db import orm_engine
from backend.database.db import Base

from backend.database.dependencies import get_db

from backend.routers.users_router import router as users_router
from backend.routers.corpus_router import router as corpus_router
from backend.routers.document_router import router as document_router
from backend.routers.search_router import router as search_router
from backend.routers.chat_router import router as chat_router


app= FastAPI()

# Create all tables when application starts
Base.metadata.create_all(bind=orm_engine)

# it makes your backend explicitly tell the browser, "It's fine, I trust requests coming from this other website"
# The frontend lives at something like domain-specific-ai-agent-frontend.onrender.com, and the backend lives at domain-knowledge-copilot-n1yc.onrender.com. 
# Different domain = different website, from the browser's point of view.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(corpus_router)
app.include_router(document_router)
app.include_router(search_router)
app.include_router(chat_router)
    
@app.get("/")
def home():
    return {"message": "Domain Knowledge Co-Pilot API"}


