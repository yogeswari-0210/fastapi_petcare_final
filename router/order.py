
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependency import get_db
from models.cart_models import Cart
from models.order_models import Order
from models.order_items_models import OrderItem
from models.product_models import Product
from schemas.order_schemas import OrderCreate, OrderRead, OrderUpdate, OrderItemCreate, OrderItemRead

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# -------------------------------
# 1️⃣ Create order (single or multiple products)
# -------------------------------
@router.post("/create", response_model=OrderRead)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    if not order.items:
        raise HTTPException(status_code=400, detail="No items in order")

    new_order = Order(user_id=order.user_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    order_items = []
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(order_item)
        order_items.append(order_item)

    db.commit()

    # attach items for response
    new_order.items = order_items
    return new_order

# -------------------------------
# 2️⃣ Create order from cart
# -------------------------------
@router.post("/create-from-cart/{user_id}", response_model=OrderRead)
def create_order_from_cart(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    new_order = Order(user_id=user_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    order_items = []
    for cart_item in cart_items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if not product:
            continue  # skip missing products

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=product.price
        )
        db.add(order_item)
        order_items.append(order_item)

        db.delete(cart_item)  # remove from cart

    db.commit()
    if not order_items:
        raise HTTPException(status_code=400, detail="No valid products in cart")

    new_order.items = order_items
    return new_order

# -------------------------------
# 3️⃣ Get all orders of a user
# -------------------------------
@router.get("/user/{user_id}", response_model=List[OrderRead])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders

# -------------------------------
# 4️⃣ Get a single order by ID
# -------------------------------
@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# -------------------------------
# 5️⃣ Update order quantity (single item)
# -------------------------------
@router.put("/update/{order_item_id}", response_model=OrderItemRead)
def update_order_item(order_item_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    order_item.quantity = order_update.quantity
    db.commit()
    db.refresh(order_item)
    return order_item

# -------------------------------
# 6️⃣ Delete an order
# -------------------------------
@router.delete("/delete/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully"}
