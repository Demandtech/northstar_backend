from .. import models, database, schemas
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from typing import List

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get('/', response_model=List[schemas.ProductOut])
def get_products(db: session = Depends(database.get_db)):
    products = db.query(models.Product).all()
    return products


@router.get('/topsellers', response_model=List[schemas.Product])
def get_product_type(db: session = Depends(database.get_db)):
    products = db.query(models.Product).filter(
        models.Product.topseller == True).all()
    return products


@router.get('/{id}', response_model=schemas.SingleProduct)
def get_single_product(id: int, db: session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if product:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Product not found")


@router.get('/type/{typestr}', response_model=List[schemas.Product])
def get_product_type(typestr: str, db: session = Depends(database.get_db)):
    products = db.query(models.Product).filter(
        models.Product.type == typestr).all()
    return products
