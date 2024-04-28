from fastapi.params import Body
import time
from fastapi import FastAPI
from passlib.context import CryptContext
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor   #importing because after running the query it should give the name of column
from . import models,schemas,utils
from .database import engine,get_db
from .routers import post, user,auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


my_posts = [{"title": "Post 1", "content": "Content 1", "id":1},
            {"title": "Post 2", "content": "Content 2", "id":2}]

while  True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='suyash@123', cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print('database connection successfull')
        break
    except Exception as error:
        print("Connection failed")
        print("error:",error)
        time.sleep(3)

def find_post(id):
    for p in my_posts:
        if p['id'] ==  id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if  p['id'] ==  id:
            return i
        
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
# so basically what is happening here is whenever we had http request after getting here it checks it line by line after getting into above line then it goes to post router and checks for a match
@app.get("/")
def root():
    return {"message": "i will start the backend now"}


 

