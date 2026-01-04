# from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from database.database import Base


# class Order(Base):
#     __tablename__ = "orders"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, index=True)
#     total_price = Column(Float)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     items = relationship("OrderItem", back_populates="order", cascade="all, delete")


from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
     
