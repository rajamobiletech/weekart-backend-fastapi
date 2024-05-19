from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from app.schemas import schemas 
from app.common import oauth2
from app.db.database import SessionLocal, engine, get_db
from app.db import models


router = APIRouter(prefix='/products', tags=['Products'])


@router.get('/', response_model=List[schemas.ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.get('/{id}', response_model=schemas.ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product is not avialble in weekart", headers={"X-Error": "User Input Error"})
    return product

@router.get('/latest/{count}', response_model=List[schemas.ProductResponse])
def get_all_products(count: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
   latest_products = db.query(models.Product).filter(models.Product.owner_id == current_user.id).order_by(models.Product.created_at.desc()).all()
   return latest_products

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.ProductResponse)
def create_post(new_product: schemas.ProductRequest, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    create_product = models.Product(owner_id=current_user.id,shippername='test', **new_product.dict())
    db.add(create_product)
    db.commit()
    db.refresh(create_product)
    return create_product

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
   
    # Fetching the product information
    product = db.query(models.Product).filter(models.Product.id == id)
    
    # If product id is not exist, throw an error
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product is not avialble in weekart", headers={"X-Error": "User Input Error"})
    
    if product.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to delete this product", headers={"X-Error": "User Input Error"})
    # Deleting the product
    product.delete()
    db.commit()

@router.put('/{id}', response_model=schemas.ProductResponse)
def update_product_by_id(id: int, product_res: schemas.ProductRequest, db: Session=Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
     # Fetching the product information
    product = db.query(models.Product).filter(models.Product.id == id)
    
    # If product id is not exist, throw an error
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product is not avialble in weekart", headers={"X-Error": "User Input Error"})
    
    if product.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to delete this product", headers={"X-Error": "User Input Error"})
    
    # Update the product using dic values
    # model_dump helps to convert into dictionary format
    product.update(product_res.model_dump())

    #Db commit to save data on DB 
    db.commit()

    #Returing the updated product 
    return product.first()