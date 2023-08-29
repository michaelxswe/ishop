from typing import Optional
from datetime import datetime, date
from schemas.base import Base
from schemas.payment import PaymentCreate, PaymentUpdate, PaymentRead
from pydantic import model_validator, Field
from fastapi import HTTPException, status

class UserCreate(Base):
   username: str
   password: str = Field(min_length=10, max_length=20)
   confirm_password: str = Field(exclude=True)
   email: str = Field(pattern=r'^[a-zA-Z0-9.]+\@[a-zA-Z]+\.[a-zA-Z]')
   dob: date
   payment: PaymentCreate

   @model_validator(mode='after')
   def populate_fields(self) -> 'UserCreate':
      if self.password != self.confirm_password:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail = 'Passwords do not match'
        )
      
      return self


class UserUpdate(Base):
   username: Optional[str] = Field(default=None)
   password: Optional[str] = Field(default=None, min_length=10, max_length=20)
   email: Optional[str] = Field(default=None, pattern=r'^[a-zA-Z0-9.]+\@[a-zA-Z]+\.[a-zA-Z]')
   dob: Optional[date] = Field(default=None)
   payment: Optional[PaymentUpdate] = Field(default=None)

class UserRead(Base):
   id: int
   username: str
   password: str
   email: str
   dob: date
   age: int = None
   date_created: datetime
   payment: PaymentRead

   @model_validator(mode='after')
   def populate_fields(self) -> 'UserRead':
      today = date.today()
      self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
      return self
   

class UserCredentials(Base):
   username: str
   password: str