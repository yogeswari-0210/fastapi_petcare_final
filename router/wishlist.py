

from fastapi import APIRouter, Depends,HTTPException,Query
from sqlalchemy.orm import Session
from typing import List

from dependency import get_db
from models.wishlist_models import Wishlist
from schemas.wishlist_schemas import WishlistCreate,WishlistRead
from models.cart_models import Cart

router = APIRouter(
    prefix="/wishlists",
    tags=["Wishlists"]
)



# -------------------------------
# Add product to wishlist
# -------------------------------
@router.post("/add", response_model=WishlistRead)
def add_to_wishlist(item: WishlistCreate, db: Session = Depends(get_db)):
    existing = db.query(Wishlist).filter(
        Wishlist.user_id == item.user_id,
        Wishlist.product_id == item.product_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product already in wishlist")

    new_item = Wishlist(user_id=item.user_id, product_id=item.product_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# -------------------------------
# Get wishlist items by user_id
# -------------------------------
@router.get("/user/{user_id}", response_model=List[WishlistRead])
def get_wishlist_by_user(user_id: int, db: Session = Depends(get_db)):
    items = db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
    return items

# -------------------------------
# Remove product from wishlist
# -------------------------------
@router.delete("/remove/{wishlist_id}")
def remove_from_wishlist(wishlist_id: int, db: Session = Depends(get_db)):
    item = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Wishlist item removed"}


# @router.post("/move-to-wishlist", response_model=WishlistRead)
# def move_cart_to_wishlist(cart_id: int, db: Session = Depends(get_db)):
#     # Fetch the cart item
#     cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
#     if not cart_item:
#         raise HTTPException(status_code=404, detail="Cart item not found")

#     # Create wishlist item
#     wishlist_item = Wishlist(
#         user_id=cart_item.user_id,
#         product_id=cart_item.product_id
#     )
#     db.add(wishlist_item)
#     db.commit()
#     db.refresh(wishlist_item)  # make sure SQLAlchemy populates 'id'

#     # Remove from cart
#     db.delete(cart_item)
#     db.commit()

#     return wishlist_item  # This will now match WishlistRead
