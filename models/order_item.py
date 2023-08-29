from database.config import Base
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import NUMERIC, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.order import Order
    from models.item import Item
    

class OrderItem(Base):
    __tablename__ = 'order_item'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, init=False)
    cost: Mapped[float] = mapped_column(NUMERIC(10, 2), index=True)
    qty: Mapped[int] = mapped_column(BIGINT)
    item_id: Mapped[int] = mapped_column(ForeignKey('item.id'), init = False)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'), init=False)
    
    item: Mapped['Item'] = relationship(back_populates='order_items', repr = False)
    order: Mapped['Order'] = relationship(back_populates='order_items', repr=False)