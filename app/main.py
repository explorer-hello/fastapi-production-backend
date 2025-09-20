from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .routers import post,user,auth

models.Base.metadata.create_all(bind = engine)

app =FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return{"status": posts}


@app.get("/")
def hello_world():
    return{"Hello" : "myself!!!!"}
