

from fastapi import APIRouter, Depends,Query,HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependency import get_db
from models.category_models import Category
from schemas.categories_schemas import CategoryCreate, CategoryRead,CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/", response_model=CategoryRead)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    To create both parent and child categories.
    parent_id=None → parent category
    parent_id=<parent_id> → child category
    """
    new_category = Category(name=category.name, parent_id=category.parent_id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/", response_model=List[CategoryRead])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


# Get category by id
# -------------------------------
@router.get("/id/{category_id}", response_model=CategoryRead)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# -------------------------------
# Get category by name
# -------------------------------
@router.get("/name/", response_model=List[CategoryRead])
def get_category_by_name(name: str = Query(..., description="Name of category to search"), 
                         db: Session = Depends(get_db)):
    categories = db.query(Category).filter(Category.name.ilike(f"%{name}%")).all()
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found with this name")
    return categories

# Update category
# -------------------------------
@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, update: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = update.name
    db.commit()
    db.refresh(category)
    return category

# -------------------------------
# Delete category
# -------------------------------
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"detail": "Category deleted successfully"}