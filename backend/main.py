from fastapi import FastAPI

from backend.database.db import orm_engine
from backend.database.db import Base

from backend.database.dependencies import get_db

from backend.routers.users_router import router as users_router
from backend.routers.document_router import router as document_router
from backend.routers.search_router import router as search_router
from backend.routers.chat_router import router as chat_router

app= FastAPI()

# Create all tables when application starts
Base.metadata.create_all(bind=orm_engine)

app.include_router(users_router)
app.include_router(document_router)
app.include_router(search_router)
app.include_router(chat_router)
    
@app.get("/")
def home():
    return {"message": "Domain Knowledge Co-Pilot API"}


