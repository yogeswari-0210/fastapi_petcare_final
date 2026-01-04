

# from pydantic import BaseModel
# from typing import Optional, List

# class CategoryCreate(BaseModel):
#     name: str
#     parent_id: Optional[int] = None  # If None → it's a parent category

# class CategoryRead(BaseModel):
#     id: int
#     name: str
#     parent_id: Optional[int] = None
#     children: List["CategoryRead"] = []

#     class Config:
#         orm_mode = True

# class CategoryUpdate(BaseModel):
#     name: str


from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class CategoryUpdate(BaseModel):
    name: str
