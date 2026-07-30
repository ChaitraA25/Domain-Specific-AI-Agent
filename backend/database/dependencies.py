from backend.database.db import orm_session

def get_db():
    db=orm_session()

    try:
        yield db
    
    finally:
        db.close()