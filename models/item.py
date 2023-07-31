from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, NUMERIC, TIMESTAMP, ENUM, BOOLEAN
from utils.enums import Category
from db.config import Base

if TYPE_CHECKING:
    from models.cart_item import CartItem
    from models.order_item import OrderItem

class Item(Base):
    __tablename__ = 'item'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, init=False)
    name: Mapped[str] = mapped_column(VARCHAR, unique=True)
    price: Mapped[float] = mapped_column(NUMERIC(10,2))
    category: Mapped[Category] = mapped_column(ENUM(Category))
    qty: Mapped[int] = mapped_column(INTEGER)
    sale: Mapped[int] = mapped_column(INTEGER, init=False, server_default=text('0'))
    date_created: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("date_trunc('second', now())"), init=False)
    deleted: Mapped[bool] = mapped_column(BOOLEAN, server_default=text('false'), init=False)

    cart_items: Mapped[list['CartItem']] = relationship(back_populates= 'item', init = False, repr=False)
    order_items: Mapped[list['OrderItem']] = relationship(back_populates= 'item', init = False, repr=False)