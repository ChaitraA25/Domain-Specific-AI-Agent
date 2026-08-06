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
        _user_and_pass = _before_at.split("://")[-1]
        _user_part, _password_part = _user_and_pass.split(":", 1)
        _masked_pw = f"{_password_part[:2]}...{_password_part[-2:]} (length={len(_password_part)})" if len(_password_part) > 4 else "too short to mask safely"
        print(f"[DEBUG] user='{_user_part}', password_masked='{_masked_pw}', host_part='{_after_at}'")
    else:
        print(f"[DEBUG] SUPABASE_DB_URL has no '@' - malformed")
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


