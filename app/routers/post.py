from multiprocessing import synchronize
from typing import Optional
from fastapi import FastAPI, Response, responses, status, HTTPException,Depends,APIRouter
from fastapi.security import OAuth2
from sqlalchemy import delete
from sqlalchemy.orm import Session
from .. import models,scheme,utils,oauth2
from ..database import get_db

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",response_model=list[scheme.PostResponce])
def root(db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts= cursor.fetchall()
    posts=db.query(models.Post).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=scheme.PostResponce)
def create_posts(post: scheme.CreatePost,db:Session = Depends(get_db),user:models.User=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s,%s,%s) RETURNING *""",
    #             (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    #conn.commit()
    print(user.id)
    
    new_post=models.Post(owner_id=user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=scheme.PostResponce)
def get_post(id: int, responce:Response,db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id= %s""",(str(id),))
    # post= cursor.fetchone()
    post= db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} not found")
    return post
       

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db:Session = Depends(get_db),user:models.User=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id= %s returning *""",(str(id),))
    # conn.commit()
    # delete_post = cursor.fetchone()
    
    print(f"Current user object: {user}, ID: {user.id}")
    post:Optional[models.Post]= db.query(models.Post).filter(models.Post.id==id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} is not present")    
    if post.owner_id != user.id: # type: ignore
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not autherised")
    
    #db.delete(post)
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    

# @app.put("/posts/{id}")
# def update_post(id:int,post:POST,db:Session = Depends(get_db)):
#     # cursor.execute("""UPDATE posts SET title= %s, content =%s, published=%s WHERE id= %s returning *""",(post.title,post.content,post. published,str(id)))
#     # conn.commit()
#     # updated_post=cursor.fetchone()
#     post_query=db.query(models.Post).filter(models.Post.id==id).first()
#     post= post_query
#     if post_query== None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} is not present")
#     post_query.update(post.,synchronize_session=False)
#     db.commit()
#     return{"data":post}

@router.put("/{id}",response_model=scheme.PostResponce)
def update_post(id: int, post: scheme.PostBase, db: Session = Depends(get_db),user:int=Depends(oauth2.get_current_user)):
    # Get the query object
    post_instance = db.query(models.Post).filter(models.Post.id == id).first()
    print(post_instance)
    # Check if post exists
    if post_instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} is not present")
    if post_instance.owner_id != user.id: # type: ignore
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not autherised")
    # Update each field individually using setattr
    update_data = post.model_dump()
    for field, value in update_data.items():
        if hasattr(post_instance, field):
            setattr(post_instance, field, value)

    # Return the updated post
    updated_post = post_instance
    return updated_post



