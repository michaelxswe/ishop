from datetime import datetime
from db.config import Base
from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import INTEGER, NUMERIC, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.order_item import OrderItem
    from models.user import User
    

class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, init=False)
    cost: Mapped[float] = mapped_column(NUMERIC(10, 2), index=True, default=0, init=False)
    date_created: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),server_default=text("date_trunc('second', now())"),init=False,)
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan", init=False, repr=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), init=False)
    user: Mapped["User"] = relationship(back_populates="orders", repr=False)
