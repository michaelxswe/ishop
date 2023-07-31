from typing import Optional
from schemas.base import Base

class CartItemRead(Base):
    item_id: int
    cost: float
    qty: int