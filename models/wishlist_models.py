from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="wishlists")  # must match User.wishlists
    product = relationship("Product", back_populates="wishlists")  # must match Product.wishlists

        # user = relationship("User", back_populates="wishlists")  # <-- expects User to have .wishlists



    # id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # user = relationship("User", back_populates="wishlist")        # matches User.wishlist
    # product = relationship("Product", back_populates="wishlist")  # matches Product.wishlist
# from sqlalchemy import Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship
# from database.database import Base

# class Wishlist(Base):
#     __tablename__ = "wishlist"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

#     user = relationship("User", back_populates="wishlist")        # matches User.wishlist
#     product = relationship("Product", back_populates="wishlist")  # matches Product.wishlist

