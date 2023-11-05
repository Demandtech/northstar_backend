from .. import models, schemas, utils, database, oauth2
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import session
import uuid
from ..config import settings

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#5EH4?$XVN9%#$pR

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exist")
    if user.password == user.re_password:
        hashed_password = utils.hash(user.password)
        verification_token = str(uuid.uuid4())

        user_data = user.model_dump(exclude={'re_password'})
        user_data["password"] = hashed_password
        user_data["verification_token"] = verification_token
        new_user = models.User(**user_data)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        verification_link = f"{settings.domain}/verify/{verification_token}"
        utils.send_verification_email(
            user.email, verification_link, 'Verify Your Email')

        return {"message": "Account created Successfully, and Verification email sent", "user": new_user}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Password does not match")


@router.post('/verify_user', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut)
def verify_user(token_request: schemas.VerifyToken, db: session = Depends(database.get_db)):

    try:
        user = db.query(models.User).filter(
            models.User.verification_token == token_request.token).first()

        if user:
            user.is_verified = True
            user.verification_token = None
            db.commit()
            db.refresh(user)

            utils.send_confirmation_email(user.email, 'http://localhost:3000/auth/login', 'Welcome to NorthStar')

            return {"message": "Account verification successful", "user": user}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Can not verify detail")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while verifying user")


@router.post('/forgot_password')
def forgot_password(payload: schemas.ForgotPassword, db: session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == payload.email).first()

    if user and user.is_verified:
        verification_token = str(uuid.uuid4())

        user.verification_token = verification_token
        verification_link = f"{settings.domain}/change_password/{verification_token}"
        db.commit()
        db.refresh(user)

        utils.send_verification_email(
            payload.email, verification_link, 'Reset Your Password')

        return {"message": f"Password reset link sent"}

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with given email: {payload.email} not found")


@router.post('/change_password', status_code=status.HTTP_205_RESET_CONTENT)
def change_password(payload: schemas.ChangePassword, db: session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.verification_token == payload.token).first()

    if user and user.is_verified:
        if payload.new_password == payload.re_new_password:
            hashed_password = utils.hash(payload.new_password)

            user.password = hashed_password
            user.verification_token = None

            db.commit()
            db.refresh(user)
            
            utils.send_confirmation_email(user.email, 'http://localhost:3000/auth/login', 'Password Changed!')

            return {"message": "Password changed successfully"}
        raise HTTPException(detail="Password not match",
                            status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(detail="User not found",
                        status_code=status.HTTP_404_NOT_FOUND)


@router.get("/me", response_model=schemas.UserOut)
def get_user(db: session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(
        models.User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with id: {id} does not exist")

    return {"message": "success", "user": user}
