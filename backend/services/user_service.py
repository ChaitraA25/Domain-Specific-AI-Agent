from sqlalchemy.orm import Session

from backend.database.models import User

from backend.auth.security import hash_password
def create_admin_user(db:Session, username:str, email:str, password:str):
    user=User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role="admin"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def create_user(db:Session, username:str, email:str, password:str):
    user=User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_email(db:Session, email:str,):
    return (
        db.query(User).filter(User.email==email).first()
    )
    
def get_user_by_username(db:Session,username:str):
    return (
        db.query(User).filter(User.username==username).first()
    )

