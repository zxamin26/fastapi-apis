from pydantic import BaseModel, ConfigDict, EmailStr,Field
from datetime import time,datetime,timedelta
from typing import Annotated

class PostBase(BaseModel):
    title: str
    content: str
    posted: bool = True

class CreatePost(PostBase):
    pass

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserData(BaseModel):
    id: int
    email: str
    created_at: datetime

class ResponsePost(PostBase):
    id: int
    user_id: int
    user: UserData
    

    model_config = ConfigDict(from_attributes=True)

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Vote(BaseModel):
    post_id: int
    vote_dir: Annotated[int, Field(ge=0,le=1)]

class PostOut(BaseModel):
    Post: ResponsePost
    votes: int

    model_config = ConfigDict(from_attributes=True)