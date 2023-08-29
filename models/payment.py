from database.config import Base
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User
    

class Payment(Base):
    __tablename__ = 'payment'
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, init=False)
    card_number: Mapped[int] = mapped_column(BIGINT)
    cvv: Mapped[int] = mapped_column(BIGINT)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), init=False)
    
    user: Mapped['User'] = relationship(back_populates='payment', repr=False)
