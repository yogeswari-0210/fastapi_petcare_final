
# from pydantic import BaseModel
# from typing import List






# class CartCreate(BaseModel):
#     user_id: int
#     product_id: int
#     quantity: int = 1

# class CartUpdate(BaseModel):
#     quantity: int

# class CartItemResponse(BaseModel):
#     id: int
#     product_id: int
#     name: str
#     price: float
#     quantity: int
#     total_price: float  

#     model_config = {"from_attributes": True}

# class CartResponseFull(BaseModel):
#     id: int
#     user_id: int
#     items: List[CartItemResponse]
#     items_price: float
#     delivery_fee: float
#     total_price: float

#     model_config = {"from_attributes": True}

# # # Moving cart item to wishlist
# # class MoveToWishlistResponse(BaseModel):
# #     message: str
# #     wishlist_item: WishlistResponse

# # # Moving wishlist item to cart
# # class MoveToCartResponse(BaseModel):
# #     message: str
# #     cart_item: CartItemResponse
# schemas/cart_schemas.py
# ffrom pydantic import BaseModel
from pydantic import BaseModel

from typing import List
from .cart_items_schemas import CartItemRead, CartItemUpdate

# Base Cart model (fields that exist in Cart table)
class CartBase(BaseModel):
    user_id: int  # user owning the cart

# Model for creating a Cart
class CartCreate(CartBase):
    pass

# Model for reading Cart (response model)
class CartRead(CartBase):
    id: int
    cart_items: List[CartItemRead] = []  # related cart items

    class Config:
        from_attributes = True
