from typing import Optional
from datetime import datetime
from utils.enums import Category
from schemas.base import Base

class ItemCreate(Base):
   name: str
   price: float
   category: Category
   qty: int

class ItemUpdate(Base):
   name: Optional[str] = None
   price: Optional[float] = None
   category: Optional[Category] = None 
   qty: Optional[int] = None  

class ItemRead(Base):
   id: int
   name: str
   price: float
   category: Category
   qty: int
   sale: int
   date_created: datetime
