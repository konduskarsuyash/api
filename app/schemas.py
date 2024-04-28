from pydantic import BaseModel,EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True
    
class PostCreate(PostBase):
    pass
 
class Post(PostBase):
    id:int
    created_at:datetime
    
    class Config:
        orm_mode=True   
        
class UserCreate(BaseModel):
    email:EmailStr   #EmailStr validates that it is valid email
    password:str

class UserOut(BaseModel):  #it gives you sqlAlchmey model but we have to change back to pydantice model so for that we use orm_mode=True
    id:int
    email:EmailStr
    created_at:datetime
    
    class Config:
        orm_mode=True   
        
        
class UserLogin(BaseModel):
    email:EmailStr
    password:str