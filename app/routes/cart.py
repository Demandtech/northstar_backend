from sqlalchemy.orm import Session
from .. import models, database, schemas, oauth2
from fastapi import status, HTTPException, Depends, APIRouter, Response

router = APIRouter(
    prefix="/users/me/cart",
    tags=["Carts"]
)


@router.get('/', response_model=schemas.CartOut, status_code=status.HTTP_200_OK)
def get_carts(db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):
    user_id = current_user.id
    try:
        carts = db.query(models.Cart).filter(
            models.Cart.user_id == current_user.id).all()
        if carts:
            total_carts = sum(cart.quantity for cart in carts)
            total_amount = sum(cart.amount for cart in carts)

            return {
                "total_carts": total_carts,
                "carts": carts,
                "total_amount": total_amount, "user_id": user_id
            }
        else:
            return {
                "total_carts": 0,
                "carts": [],
                "total_amount": 0,
                "user_id": user_id
            }
            # raise HTTPException(
            #     status_code=status.HTTP_404_NOT_FOUND, detail=f"No item with user with id: {user_id} found")
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No item with user with id: {user_id} found")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Cart)
def add_cart(product: schemas.CreateCart, db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):

    added_product = db.query(models.Product).filter(
        models.Product.id == product.product_id).first()

    if added_product:
        bonus_price = added_product.price - \
            (added_product.bonus * added_product.price / 100)

        existed_cart_item = db.query(models.Cart).filter(
            models.Cart.product_id == product.product_id, models.Cart.user_id == current_user.id).first()

        if existed_cart_item:
            existed_cart_item.quantity += 1
            existed_cart_item.amount = bonus_price * existed_cart_item.quantity
            db.commit()
            db.refresh(existed_cart_item)
            return existed_cart_item

        new_cart = models.Cart(
            product_id=product.product_id, user_id=current_user.id)
        new_cart.quantity = 1
        new_cart.size = product.product_size
        new_cart.amount = bonus_price * new_cart.quantity
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        return new_cart

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(id: int, db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):
    items = db.query(models.Cart).filter(models.Cart.id == id,
                                         models.Cart.user_id == current_user.id)

    item = items.first()

    if item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not authorize to delete item with id: {id}")
    items.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
