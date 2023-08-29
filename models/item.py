from datetime import datetime
from database.config import Base
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import VARCHAR, BIGINT, NUMERIC, TIMESTAMP, ENUM, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from utils.enums import Category
if TYPE_CHECKING:
    from models.cart_item import CartItem
    from models.order_item import OrderItem

class Item(Base):
    __tablename__ = 'item'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, init=False)
    name: Mapped[str] = mapped_column(VARCHAR, unique=True)
    price: Mapped[float] = mapped_column(NUMERIC(10,2))
    category: Mapped[Category] = mapped_column(ENUM(Category))
    qty: Mapped[int] = mapped_column(BIGINT)
    sale: Mapped[int] = mapped_column(BIGINT, init=False, server_default=text('0'))
    date_created: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("date_trunc('second', now())"), init=False)
    deleted: Mapped[bool] = mapped_column(BOOLEAN, server_default=text('false'), init=False)

    cart_items: Mapped[list['CartItem']] = relationship(back_populates= 'item', init = False, repr=False)
    order_items: Mapped[list['OrderItem']] = relationship(back_populates= 'item', init = False, repr=False)