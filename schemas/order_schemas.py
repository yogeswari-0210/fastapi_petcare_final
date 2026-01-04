# from pydantic import BaseModel
# from typing import List

# class OrderBase(BaseModel):
#     user_id: int
#     product_id: int
#     quantity: int = 1

# class OrderCreate(OrderBase):
#     pass



# class OrderRead(BaseModel):
#     id: int
#     user_id: int
#     product_id: int
#     quantity: int

#     class Config:
#         from_attributes = True


# class OrderUpdate(BaseModel):
#     quantity: int
# from pydantic import BaseModel

# # For single product order
# class OrderBase(BaseModel):
#     user_id: int
#     product_id: int
#     quantity: int = 1

# class OrderCreate(OrderBase):
#     pass

# class OrderRead(BaseModel):
#     id: int
#     user_id: int
#     product_id: int
#     quantity: int

#     class Config:
#         from_attributes = True

# class OrderUpdate(BaseModel):
    # quantity: int
from pydantic import BaseModel
from typing import List

# Individual product in an order
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class OrderItemRead(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

# Create order (single or multiple items)
class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]

class OrderRead(BaseModel):
    id: int
    user_id: int
    items: List[OrderItemRead] = []

    class Config:
        from_attributes = True

# Update order quantity (for single product in order)
class OrderUpdate(BaseModel):
    quantity: int



