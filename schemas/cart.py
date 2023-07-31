from schemas.base import Base
from schemas.cart_item import CartItemRead

class CartRead(Base):
    cost: float
    cart_items: list[CartItemRead]
    

   