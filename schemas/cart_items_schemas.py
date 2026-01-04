# from pydantic import BaseModel

# class CartItemBase(BaseModel):
#     cart_id: int
#     product_id: int
#     quantity: int = 1

# class CartItemCreate(CartItemBase):
#     pass

# class CartItemRead(CartItemBase):
#     id: int

#     class Config:
#         from_attributes = True


from pydantic import BaseModel, Field

# Base model (shared fields for cart item)
class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1

# Model for creating a cart item
class CartItemCreate(CartItemBase):
    pass

# Model for reading cart item (response model)
# class CartItemRead(CartItemBase):
#     id: int = Field(..., alias="cart_id")  # maps SQLAlchemy Cart.id -> cart_id

#     class Config:
#         from_attributes = True  # FastAPI v2 replacement for orm_mode

# Model for updating quantity
class CartItemUpdate(BaseModel):
    quantity: int
 


#  from pydantic import BaseModel

class CartItemRead(BaseModel):
    id: int          # matches Cart.id
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

