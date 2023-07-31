from typing import Optional
from datetime import datetime
from schemas.base import Base
from schemas.payment import PaymentCreate, PaymentUpdate, PaymentRead

class UserCreate(Base):
   username: str
   password: str
   email: str
   payment: PaymentCreate

class UserUpdate(Base):
   username: Optional[str] = None
   password: Optional[str] = None
   email: Optional[str] = None
   payment: Optional[PaymentUpdate] = None

class UserRead(Base):
   id: int
   username: str
   password: str
   email: str
   date_created: datetime
   payment: PaymentRead

class UserCredentials(Base):
   username: str
   password: str