from typing import Optional
from schemas.base import Base

class OrderItemRead(Base):
    item_id: int
    cost: float
    qty: int