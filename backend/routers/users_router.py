from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db

from backend.schemas.user_schema import UserCreate,UserResponse,UserLogin

from backend.services.user_service import create_user as create_user_service,create_admin_user as create_admin_service,get_user_by_email ,get_user_by_username

from backend.auth.security import verify_password
from backend.auth.jwt_handler import create_access_token

from backend.auth.dependencies import get_current_user
from backend.database.models import User
from fastapi.security import OAuth2PasswordRequestForm

# creates a router object
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Database session created successfully"}

@router.post("/create-admin",response_model=UserResponse)
def create_admin(user:UserCreate,db:Session = Depends(get_db)):
    
    existing_email = get_user_by_email(db,user.email)

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    existing_username = get_user_by_username(db,user.username)

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    return create_admin_service(db=db,
            username=user.username,
            email=user.email,
            password=user.password
        )

@router.post("/",response_model=UserResponse)
def create_user(user:UserCreate,db:Session = Depends(get_db)):
    
    existing_email = get_user_by_email(db,user.email)

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    existing_username = get_user_by_username(db,user.username)

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    return create_user_service(db=db,
            username=user.username,
            email=user.email,
            password=user.password
        )

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = get_user_by_email(db,form_data.username)

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

