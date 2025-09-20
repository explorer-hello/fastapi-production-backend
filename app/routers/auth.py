from fastapi import APIRouter,Depends,status,HTTPException,Response 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,scheme,models,utils,oauth2


router=APIRouter(tags=["Authentication"])

@router.post("/login",response_model=scheme.Token)
def login_user(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid user")
    
    if not utils.verifyPassword(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credentials")
    
    #create token
    #return token

    access_token=oauth2.create_access_token(data={"user_id":user.id})
    return {
    "access_token": access_token,
    "token_type": "bearer"
}

