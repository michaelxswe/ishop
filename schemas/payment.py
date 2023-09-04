from typing import Optional
from schemas.base import Base

class PaymentCreate(Base):
   card_number: str
   cvv: str

class PaymentUpdate(Base):
   card_number: Optional[str] = None
   cvv: Optional[str] = None  

class PaymentRead(Base):
   id: int
   card_number: str
   cvv: str