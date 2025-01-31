from database.config import Base
from sqlalchemy import text, ForeignKey
from sqlalchemy.dialects.postgresql import NUMERIC, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.cart_item import CartItem
    from models.user import User


class Cart(Base):
    __tablename__ = 'cart'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, init=False)
    cost: Mapped[float] = mapped_column(NUMERIC(10, 2), index=True, init=False, server_default=text('0'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), init=False)

    cart_items: Mapped[list['CartItem']] = relationship(back_populates='cart', init=False, repr=False)
    user: Mapped['User'] = relationship(back_populates='cart', repr=False)