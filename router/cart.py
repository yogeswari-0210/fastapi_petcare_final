
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependency import get_db
from models.cart_models import Cart
from models.user_models import User
from schemas.cart_schemas import CartCreate,CartItemRead ,CartItemUpdate
from schemas. cart_items_schemas import CartItemBase,CartItemCreate,CartItemUpdate

router = APIRouter(
    prefix="/carts",
    tags=["Carts"]
)


@router.get("/", response_model=List[CartCreate])
def get_carts(db: Session = Depends(get_db)):
    return db.query(Cart).all()





@router.post("/add", response_model=CartItemRead)
def add_to_cart(cart_item: CartItemCreate, user_id: int, db: Session = Depends(get_db)):
    existing_item = db.query(Cart).filter(
        Cart.user_id == user_id, 
        Cart.product_id == cart_item.product_id
    ).first()
    if existing_item:
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    new_item = Cart(
        user_id=user_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# -------------------------------
# Get all cart items for a user by username
# -------------------------------
@router.get("/user/byname/{username}", response_model=List[CartItemRead])
def get_cart_items_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(Cart).filter(Cart.user_id == user.id).all()

# -------------------------------
# Get all cart items for a user by user_id
# -------------------------------
@router.get("/user/{user_id}", response_model=List[CartItemRead])
def get_cart_items_by_userid(user_id: int, db: Session = Depends(get_db)):
    return db.query(Cart).filter(Cart.user_id == user_id).all()

# # -------------------------------
# # Remove a single cart item
# # -------------------------------
# @router.delete("/remove/{cart_item_id}")
# def remove_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
#     item = db.query(Cart).filter(Cart.id == cart_item_id).first()
#     if not item:
#         raise HTTPException(status_code=404, detail="Cart item not found")
#     db.delete(item)
#     db.commit()
#     return {"detail": "Cart item removed successfully"}

# -------------------------------
# Update quantity of a cart item
# -------------------------------
# @router.put("/update/{cart_item_id}", response_model=CartItemRead)
# def update_cart_item(cart_item_id: int, cart_item: CartItemUpdate, db: Session = Depends(get_db)):
#     item = db.query(Cart).filter(Cart.id == cart_item_id).first()
#     if not item:
#         raise HTTPException(status_code=404, detail="Cart item not found")
#     item.quantity = cart_item.quantity
#     db.commit()
#     db.refresh(item)
#     return item
