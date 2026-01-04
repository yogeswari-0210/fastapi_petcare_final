# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from dependency import get_db
# from models.cart_items_models import CartItem
# from models.cart_models import Cart
# from models.product_models import Product
# from models.user_models import User
# from models.wishlist_models import Wishlist
# from schemas.cart_schemas import CartItemCreate, CartItemResponse

# router = APIRouter(
#     prefix="/cart-items",
#     tags=["Cart Items"]
# )

# # Add item to cart (for a given user)
# @router.post("/{user_id}", response_model=CartItemResponse)
# def add_cart_item(user_id: int, item_data: CartItemCreate, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     product = db.query(Product).filter(Product.id == item_data.product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")

#     # Get user's active cart
#     cart = db.query(Cart).filter(Cart.user_id == user_id, Cart.status == "active").first()
#     if not cart:
#         cart = Cart(user_id=user_id)
#         db.add(cart)
#         db.commit()
#         db.refresh(cart)

#     # Check if product already in cart
#     cart_item = db.query(CartItem).filter(
#         CartItem.cart_id == cart.id,
#         CartItem.product_id == item_data.product_id
#     ).first()

#     if cart_item:
#         cart_item.quantity += item_data.quantity
#     else:
#         cart_item = CartItem(
#             cart_id=cart.id,
#             product_id=item_data.product_id,
#             quantity=item_data.quantity
#         )
#         db.add(cart_item)

#     db.commit()
#     db.refresh(cart_item)

#     return CartItemResponse(
#         product_id=product.id,
#         name=product.name,
#         price=product.price,
#         quantity=cart_item.quantity,
#         total_price=product.price * cart_item.quantity
#     )

# # Update quantity
# @router.put("/{cart_item_id}", response_model=CartItemResponse)
# def update_cart_item(cart_item_id: int, item_data: CartItemCreate, db: Session = Depends(get_db)):
#     cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
#     if not cart_item:
#         raise HTTPException(status_code=404, detail="Cart item not found")

#     cart_item.quantity = item_data.quantity
#     db.commit()
#     db.refresh(cart_item)

#     return CartItemResponse(
#         product_id=cart_item.product.id,
#         name=cart_item.product.name,
#         price=cart_item.product.price,
#         quantity=cart_item.quantity,
#         total_price=cart_item.product.price * cart_item.quantity
#     )

# # Delete item
# @router.delete("/{cart_item_id}")
# def delete_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
#     cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
#     if not cart_item:
#         raise HTTPException(status_code=404, detail="Cart item not found")

#     db.delete(cart_item)
#     db.commit()
#     return {"message": "Cart item deleted successfully"}

# # Move item to wishlist
# @router.post("/move-to-wishlist/{user_id}/{cart_item_id}")
# def move_to_wishlist(user_id: int, cart_item_id: int, db: Session = Depends(get_db)):
#     cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
#     if not cart_item:
#         raise HTTPException(status_code=404, detail="Cart item not found")

#     # Check if product already in wishlist
#     existing = db.query(Wishlist).filter_by(
#         user_id=user_id,
#         product_id=cart_item.product_id
#     ).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Product already in wishlist")

#     wishlist_item = Wishlist(
#         user_id=user_id,
#         product_id=cart_item.product_id
#     )
#     db.add(wishlist_item)
#     db.delete(cart_item)
#     db.commit()

#     return {"message": "Moved to wishlist successfully", "product_id": cart_item.product_id}
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from dependency import get_db
from models.cart_items_models import CartItem
from schemas.cart_items_schemas import CartItemCreate

router = APIRouter(
    prefix="/cart-items",
    tags=["CartItems"]
)

@router.post("/", response_model=CartItemCreate)
def add_cart_item(item: CartItemCreate, db: Session = Depends(get_db)):
    new_item = CartItem(cart_id=item.cart_id, product_id=item.product_id, quantity=item.quantity)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/", response_model=List[CartItemCreate])
def get_cart_items(db: Session = Depends(get_db)):
    return db.query(CartItem).all()
