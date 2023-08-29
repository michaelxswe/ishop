from database.config import Base
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import NUMERIC, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.cart import Cart
    from models.item import Item


class CartItem(Base):
    __tablename__ = 'cart_item'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, init=False)
    cost: Mapped[float] = mapped_column(NUMERIC(10, 2), index=True)
    qty: Mapped[int] = mapped_column(BIGINT)
    item_id: Mapped[int] = mapped_column(ForeignKey('item.id'), init=False)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'), init=False)

    item: Mapped["Item"] = relationship(back_populates="cart_items", repr=False)
    cart: Mapped["Cart"] = relationship(back_populates='cart_items', repr=False)