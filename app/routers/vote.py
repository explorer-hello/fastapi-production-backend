from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy import false 
from .. import models,scheme,oauth2,database
from sqlalchemy.orm import Session



router =APIRouter(
    prefix="/vote",
    tags=['vote']
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:scheme.Vote,db:Session=Depends(database.get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {vote.post_id} does not exist")
    
    print(f"Current user object: {current_user}, ID: {current_user.id}")
    current_id=current_user.id #type:ignore
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_id) 
    found_vote= vote_query.first()
    if (vote.dir== 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"the user with id {current_id}has already voted on this post{vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id,user_id= current_id)
        db.add(new_vote)
        db.commit()
        return {"message":"succesfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exists")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"succesfully deleted vote"}

