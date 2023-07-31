from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import NUMERIC, INTEGER
from db.config import Base

if TYPE_CHECKING:
    from models.order import Order
    from models.item import Item

class OrderItem(Base):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, init=False)
    cost: Mapped[float] = mapped_column(NUMERIC(10, 2), index=True)
    qty: Mapped[int] = mapped_column(INTEGER)

    item_id: Mapped[int] = mapped_column(ForeignKey('item.id'), init = False)
    item: Mapped['Item'] = relationship(back_populates='order_items', repr = False)

    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'), init=False)
    order: Mapped['Order'] = relationship(back_populates='order_items', repr=False)