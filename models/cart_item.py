from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import NUMERIC, INTEGER
from db.config import Base

if TYPE_CHECKING:
    from models.cart import Cart
    from models.item import Item
    
class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, init=False)
    cost: Mapped[float] = mapped_column(NUMERIC(10, 2), index=True)
    qty: Mapped[int] = mapped_column(INTEGER)

    item_id: Mapped[int] = mapped_column(ForeignKey('item.id'), init = False)
    item: Mapped['Item'] = relationship(back_populates='cart_items', repr = False)

    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'), init=False)
    cart: Mapped['Cart'] = relationship(back_populates='cart_items', repr=False)