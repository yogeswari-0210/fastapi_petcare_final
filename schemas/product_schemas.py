from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: int
    category_id: Optional[int]

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True





