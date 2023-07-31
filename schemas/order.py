from schemas.base import Base
from datetime import datetime
from schemas.order_item import OrderItemRead

class OrderRead(Base):
    id: int
    cost: float
    order_items: list[OrderItemRead]
    date_created: datetime