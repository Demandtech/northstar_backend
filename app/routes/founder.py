from .. import models, database, schemas
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from typing import List


router = APIRouter(
    prefix="/founders",
    tags=["Founders"]
)


@router.get('/', response_model=List[schemas.Founder])
def get_founders(db: session = Depends(database.get_db)):
    founders = db.query(models.Founder).all()
    return founders
