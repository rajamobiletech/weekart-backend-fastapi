from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.common import oauth2
from app.schemas import schemas
from app.db import models
from app.db.database import get_db
from app.common import utils


router = APIRouter(prefix='/login', tags=['Login'])


@router.post('/')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = db.query(models.User).filter(user_credentials.username == models.User.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Username.")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password.")
    
    token =  oauth2.create_access_token(data={"user_id": user.id, "username": user.username})
    return {"access_token": token, "token_type": "Bearer"}
    

