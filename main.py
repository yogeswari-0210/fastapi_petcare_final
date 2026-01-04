from fastapi import FastAPI
from database.database import Base, engine
from models import user_models, product_models

from router.user import router as users
from router.product import router as products
from router.cart import router as cart
from router.category import router as categories
from router.wishlist import router as wishlist
from router.order import router as order






app = FastAPI()

from models import (
    user_models,
    product_models,
    cart_models,
    cart_items_models,
    category_models,
    wishlist_models,
    order_models,
    order_items_models  
)

Base.metadata.create_all(bind=engine)

app.include_router(users)
app.include_router(products)
app.include_router(cart)
app.include_router(categories)
app.include_router(wishlist) 
app.include_router(order)


