# JSON Web To - secure way to identify a user after login without storing session data on the server.
from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone

import os

from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode=data.copy()

    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_token(token:str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=ALGORITHM
        )
        return payload
    except JWTError:
        return None
