from fastapi import FastAPI

from backend.database.db import orm_engine
from backend.database.db import Base

from backend.database.dependencies import get_db

from backend.routers.users_router import router as users_router
from backend.routers.corpus_router import router as corpus_router
from backend.routers.document_router import router as document_router
from backend.routers.search_router import router as search_router
from backend.routers.chat_router import router as chat_router

import os

_debug_url = os.getenv("SUPABASE_DB_URL", "")
if _debug_url:
    if "@" in _debug_url:
        _before_at, _after_at = _debug_url.rsplit("@", 1)
        _user_part = _before_at.split("://")[-1].split(":")[0]
        print(f"[DEBUG] SUPABASE_DB_URL length={len(_debug_url)}, user='{_user_part}', host_part='{_after_at}'")
    else:
        print(f"[DEBUG] SUPABASE_DB_URL length={len(_debug_url)}, no '@' found - likely malformed")
else:
    print("[DEBUG] SUPABASE_DB_URL is empty or not set!")
    
app= FastAPI()

# Create all tables when application starts
Base.metadata.create_all(bind=orm_engine)

app.include_router(users_router)
app.include_router(corpus_router)
app.include_router(document_router)
app.include_router(search_router)
app.include_router(chat_router)
    
@app.get("/")
def home():
    return {"message": "Domain Knowledge Co-Pilot API"}


