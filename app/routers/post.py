from .. import models,schemas,oauth2
from typing import List,Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm  import Session
from ..database import get_db
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix='/posts', # this is we  are making because it is hard for when we create a new @router then we have to write the same thing again again 
    tags=['Posts']   # this is just for simplicity for the localhost:8000/docs where yiu will have a good ui
)

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.Post])
def posts(db:Session = Depends(get_db),limit:int=10,skip:int=0,search:Optional[str]=""):
    
    # cursor.execute("""SELECT * FROM post """)
    # posts = cursor.fetchall() this is with using raw sql
 
    posts =  db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
    return posts





@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO post (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id  ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # this is doing the returning work that is been done in above query
    return new_post 



@router.get('/{id}',response_model=schemas.Post)
def  get_post(id:int,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM post WHERE  id=%s""",str(id))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id:{id} not found')
    return post



@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM post WHERE  id=%s RETURNING * """,str(id))
    # delete_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id:{id} does not exist')
     
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="NO t authorized to perform this action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} does not exist')
    
    print("post owner id *******",post.owner_id)
    print("post user id *****",current_user.id)
    
    # Now you can access post.owner to get the user who created the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    
    # Update the post
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()
