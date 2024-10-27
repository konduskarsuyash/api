from fastapi.params import Body
import time
from fastapi import FastAPI
from passlib.context import CryptContext
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor   #importing because after running the query it should give the name of column
from . import models,schemas,utils
from .database import engine,get_db
from .routers import post, user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost:5173",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
        
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

# so basically what is happening here is whenever we had http request after getting here it checks it line by line after getting into above line then it goes to post router and checks for a match
@app.get("/")
def root():
    return {"message": "i will start the backend now"}


 

