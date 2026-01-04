

from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from typing import List

from dependency import get_db
from models.product_models import Product
from schemas.product_schemas import ProductCreate,ProductRead
from models.category_models import Category
from schemas.order_schemas import OrderRead
from models.order_models import Order

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(name=product.name, price=product.price, category_id=product.category_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[ProductCreate])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/name/{product_name}", response_model=List[ProductRead])
def get_product_by_name(product_name: str, db: Session = Depends(get_db)):
    products = db.query(Product).filter(
        Product.name.ilike(f"%{product_name}%")
    ).all()
    return products

# @router.get("/category/{category_name}", response_model=List[ProductRead])
# def get_products_by_category(category_name: str, db: Session = Depends(get_db)):
#     products = (
#         db.query(Product)
#         .join(Category)
#         .filter(Category.name.ilike(f"%{category_name}%"))
#         .all()
#     )
#     return products


@router.get("/category/{category_name}", response_model=List[ProductRead])
def get_products_by_category(category_name: str, db: Session = Depends(get_db)):
    products = (
        db.query(Product)
        .join(Category)
        .filter(Category.name.ilike(f"%{category_name}%"))
        .all()
    )
    if not products:
        raise HTTPException(status_code=404, detail=f"No products found for category '{category_name}'")
    return products



@router.get("/filter/price", response_model=List[ProductRead])
def filter_products_by_price(
    min_price: float = Query(0),
    max_price: float = Query(100000),
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.price >= min_price,
        Product.price <= max_price
    ).all()
    return products


@router.post("/orders/create/{user_id}", response_model=OrderRead)
def create_order(user_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    new_order = Order(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
