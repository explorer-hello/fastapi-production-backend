import email_validator
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at:datetime

    class Config:
        orm_mode= True



class PostBase(BaseModel):
    title : str
    content : str
    published : bool = False
    

class CreatePost(PostBase):
    pass

class PostResponce(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner: UserOut

    class Config:
        orm_mode= True

class CreateUSer(BaseModel):
    email:EmailStr
    password:str





class loginUser(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class Token_data(BaseModel):
    id:Optional[str]=None

