# models/cartitems_models.py
# from sqlalchemy import Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship
# from database.database import Base

# class CartItem(Base):
#     __tablename__ = "cart_items"

#     id = Column(Integer, primary_key=True, index=True)

#     # ✅ REQUIRED foreign key
#     cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)

#     product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
#     quantity = Column(Integer, default=1)

#     # ✅ relationships
#     cart = relationship("Cart", back_populates="cart_items")
#     product = relationship("Product", back_populates="cart_items")
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Relationships
    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
# product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

