from fastapi import APIRouter, HTTPException, status
from db.config import engine, Base
from utils.logger import logger
from schemas.message import Message

from models.item import Item
from models.cart import Cart
from models.cart_item import CartItem
from models.order import Order
from models.order_item import OrderItem
from models.user import User
from models.payment import Payment

router = APIRouter(prefix='/api/root', tags = ['root'])

@router.get('/create_all_tables', response_model=Message)
async def create_all_tables():
   try:
      Base.metadata.create_all(bind=engine)
      logger.info('All tables are created')
      return Message(message='All tables are created')
   
   except Exception as exc:
      logger.error(str(exc))
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@router.get('/drop_all_tables', response_model=Message)
async def drop_all_tables():
   try:
      Base.metadata.drop_all(bind=engine)
      logger.info('All tables are dropped')
      return Message(message='All tables are dropped')
   
   except Exception as exc:
      logger.error(str(exc))
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))