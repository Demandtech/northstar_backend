from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from datetime import datetime


class Product(BaseModel):
    id: int
    bonus: float
    categories: list
    description: str
    img: str
    name: str
    price: float
    rating: float
    review: int
    tags: list
    thumbnails: list
    topseller: bool
    type: str


class ProductOut(BaseModel):
    id: int
    img: str
    name: str
    price: float


class SingleProduct(BaseModel):
    id: int
    bonus: float
    categories: list
    description: str
    img: str
    name: str
    price: float
    rating: float
    review: int
    tags: list
    thumbnails: list
    topseller: bool
    type: str
    sizes: list


class Cart(BaseModel):
    id: int
    created_at: datetime
    product_id: int
    quantity: int
    amount: float
    user_id: int
    product: Product
    size: str


class CreateCart(BaseModel):
    product_id: int
    product_size: str


class CartOut(BaseModel):
    total_carts: int
    total_amount: float
    user_id: int
    carts: List[Cart]


class Founder(BaseModel):
    id: int
    img: str
    name: str


class Testimony(BaseModel):
    id: int
    img: str
    name: str
    text: str


# class User(BaseModel):
#     id: int
#     email: EmailStr
#     password: str
#     address: Optional[dict]
#     billing_address: Optional[dict]
#     phone_number: Optional[str]
#     created_at: datetime
#     last_name: str
#     first_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    re_password: str
    last_name: str
    first_name: str


class User(BaseModel):
    id: int
    email: EmailStr
    last_name: str
    first_name: str
    address: Optional[dict]
    created_at: datetime
    billing_address: Optional[dict]
    phone_number: Optional[str]


class UserOut(BaseModel):
    message: str
    user: User


class ForgotPassword(BaseModel):
    email: EmailStr


class ChangePassword(BaseModel):
    token: str
    new_password: str
    re_new_password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class VerifyToken(BaseModel):
    token: str
