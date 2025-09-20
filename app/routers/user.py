from typing import Dict
from fastapi import FastAPI, Response, responses, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,scheme,utils
from ..database import get_db

router= APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=scheme.UserOut)
def Create_user(user:scheme.CreateUSer,db: Session = Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password


    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    #user_exists=False
    return new_user


@router.get("/{id}",response_model=scheme.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=print(f"user with {id} does not exist"))
    return user
