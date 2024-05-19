from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated


from pydantic.types import conint

class ProductBase(BaseModel):
    product_name: str
    price: int
    category: str
    image_url: str
    discount: int

# This schema used for product create request
class ProductRequest(ProductBase):
    pass


class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone: str

class UserRequest(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# This schema used for product response (Get, Post, Delete, update)
class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    product_id: int
    # dir: conint(le=1)
    dir: Annotated[int, Field(strict=True, le=1)]