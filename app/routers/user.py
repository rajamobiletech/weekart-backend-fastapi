from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.db.database import get_db
from app.db import models
from app.common import utils

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_post(new_user: schemas.UserRequest, db: Session = Depends(get_db)):
    new_user.password = utils.hash_password(new_user.password)
    create_user = models.User(**new_user.dict())
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user

@router.get('/{id}', response_model=schemas.UserResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found", headers={"X-Error": "User Input Error"})
    return user
