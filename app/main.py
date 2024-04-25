from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
import time
from typing import Optional
from sqlalchemy.orm  import Session
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor   #importing because after running the query it should give the name of column
from . import models,schemas
from .database import engine,get_db

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

@app.get("/")
def root():
    return {"message": "i will start the backend now"}

@app.get('/sqlalchemy')
def test_posts(db:Session = Depends(get_db)):
    posts =  db.query(models.Post).all()
    return {'data':posts}

@app.get("/posts")
def posts(db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM post """)
    # posts = cursor.fetchall() this is with using raw sql
 
    posts =  db.query(models.Post).all() 
    return {"data":posts}



@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(post:schemas.Post, db:Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO post (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # this is doing the returning work that is been done in above query
    return {"data":new_post }



@app.get('/posts/{id}')
def  get_post(id:int,db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM post WHERE  id=%s""",str(id))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id:{id} not found')
    return {"post_detail":post}



@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM post WHERE  id=%s RETURNING * """,str(id))
    # delete_post = cursor.fetchone()
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id==id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id:{id} does not exist')
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id:int,updated_post:schemas.Post,db:Session = Depends(get_db)):
    # cursor.execute("""UPDATE post SET title=%s,content=%s,published=%s WHERE id = %sRETURNING *""",
    # (post.title,post.content,post.published,str(id)))
    # update_post=cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id:{id} does not exist')
   
   
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return {"data":post_query.first( )}
