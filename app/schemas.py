from pydantic import BaseModel, EmailStr, validator, ValidationError
from typing import Optional
from datetime import datetime



 
class UserBase(BaseModel):
    username: str
    

class UserCreate(UserBase):
    email: EmailStr
    password: str
    
    class Config:
        from_attributes = True
    
class UserCrtResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserGet(UserBase):
    id: int
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None 
    
class ItemBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False

class Post(ItemBase):
    id: int
    created_at: datetime
    owner: UserCreate

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        from_attributes = True
        
class Vote(BaseModel):
    post_id: int
    dir: int
    
    @validator("dir")
    def must_be_zero_or_one(cls, v):
        if v not in (0, 1):
            raise ValueError("Must be value 1 or 0")
        return v