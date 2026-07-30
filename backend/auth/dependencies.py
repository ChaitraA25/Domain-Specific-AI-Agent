from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.auth.jwt_handler import verify_token
from backend.services.user_service import get_user_by_email


oauth2_scheme  = OAuth2PasswordBearer(tokenUrl="/users/login")
"""
Authorization code 
"""

def get_current_user(
    token : str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    user = get_user_by_email(db, email)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user