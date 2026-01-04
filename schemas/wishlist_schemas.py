from pydantic import BaseModel
from typing import List

class WishlistBase(BaseModel):
    user_id: int
    product_id: int

class WishlistCreate(WishlistBase):
    pass

from pydantic import BaseModel

class WishlistRead(BaseModel):
    id: int
    user_id: int
    product_id: int

    class Config:
        from_attributes = True  # important for ORM models

