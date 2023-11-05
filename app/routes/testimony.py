from .. import models, database, schemas
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from typing import List


router = APIRouter(
    prefix="/testimony",
    tags=["Testimonials"]
)


@router.get('/', response_model=List[schemas.Testimony])
def get_testimony(db: session = Depends(database.get_db)):
    testimonies = db.query(models.Testimonial).all()
    return testimonies
