from typing import TYPE_CHECKING
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import NUMERIC, INTEGER
from db.config import Base

if TYPE_CHECKING:
    from models.cart_item import CartItem
    from models.user import User

class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, init=False)
    cost: Mapped[float] = mapped_column(NUMERIC(10, 2), index=True, init = False, server_default=text('0'))

    cart_items: Mapped[list['CartItem']] = relationship(back_populates= 'cart', init=False, repr=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), init=False)
    user: Mapped['User'] = relationship(back_populates='cart', repr=False)