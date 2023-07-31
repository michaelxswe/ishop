from typing import Optional
from schemas.base import Base

class PaymentCreate(Base):
   card_number: int
   cvv: int

class PaymentUpdate(Base):
   card_number: Optional[int] = None
   cvv: Optional[int] = None  

class PaymentRead(Base):
   id: int
   card_number: int
   cvv: int