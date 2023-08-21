from datetime import datetime, date
from db.config import Base
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ENUM, INTEGER, TIMESTAMP, VARCHAR, DATE
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from utils.enums import Role
if TYPE_CHECKING:
    from models.cart import Cart
    from models.order import Order
    from models.payment import Payment
    

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, init=False)
    username: Mapped[str] = mapped_column(VARCHAR, unique=True)
    password: Mapped[str] = mapped_column(VARCHAR)
    email: Mapped[str] = mapped_column(VARCHAR, unique=True)
    role: Mapped[Role] = mapped_column(ENUM(Role))
    dob: Mapped[date] = mapped_column(DATE)
    date_created: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),server_default=text("date_trunc('second', now())"),init=False,)
    payment: Mapped["Payment"] = relationship(back_populates="user", init=False, cascade="all, delete-orphan", repr=False)
    cart: Mapped["Cart"] = relationship(back_populates="user", init=False, cascade="all, delete-orphan", repr=False)
    orders: Mapped[list["Order"]] = relationship(back_populates="user", init=False, cascade="all, delete-orphan", repr=False)