from pydantic import BaseModel,EmailStr
#Represents API structure

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id:int
    username: str
    email: EmailStr
    role: str

    # SQLAlchemy model User is an object , and pydantic gives response in dictionary
    # To avoid conflict, "from_attributes = True" tells Pydantic that it can create a schema object from an object's attributes
    #Config should be a nested class inside the schema class, for the UserResponse to use it.
    class Config:
        from_attributes=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
