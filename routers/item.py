from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from db.session import get_session
from utils.logger import logger
from utils.security import authenticate_token, validate_user
from schemas.item import ItemCreate, ItemRead
from schemas.cart import CartRead
from schemas.order import OrderRead
from schemas.message import Message
from models.item import Item
from models.cart_item import CartItem
from models.order_item import OrderItem
from models.order import Order

router = APIRouter(prefix='/api/item', tags = ['item'])

@router.post('/add_item', response_model= Message)
async def add_item(data: ItemCreate, response: Response, session: Session = Depends(get_session)):
   try:
      
      if session.execute(select(Item).where(Item.name == data.name)).scalar() != None:
         response.status_code = status.HTTP_409_CONFLICT
         return Message(message='Name already exist')
      
      item = Item(**data.model_dump())
      session.add(item)
      session.commit()
      logger.info(f'Item(id: {item.id}) is added')
      return Message(message='Item is added')
      
   except Exception as exc:
      session.rollback()
      logger.error(str(exc))
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@router.get('/get_item{item_id}', response_model=ItemRead | Message)
async def get_item(item_id: int, response: Response, session: Session = Depends(get_session)):
   try:
      product = session.execute(select(Item).where(Item.id == item_id, Item.deleted == False)).scalar()
      if product == None:
         response.status_code = status.HTTP_404_NOT_FOUND
         return Message(message='Item not found')
      
      return product

   except Exception as exc:
      session.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(exc))
   
@router.get('/get_all_items', response_model=list[ItemRead] | Message)
async def get_all_products(session: Session = Depends(get_session)):
   try:
      all_products = session.execute(select(Item).where(Item.deleted == False)).scalars().fetchall()
      return all_products

   except Exception as exc:
      session.rollback()
      logger.error(str(exc))
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(exc))
   

@router.get('/add_to_cart/{item_id}/{qty}', response_model=Message)
async def add_to_cart(item_id: int, qty: int, response: Response, user_id: int = Depends(authenticate_token), session: Session = Depends(get_session)):
   curr_user = validate_user(user_id=user_id, session=session)
   try:
      item = session.execute(select(Item).where(Item.id == item_id, Item.deleted == False)).scalar()
      if item == None:
         response.status_code = status.HTTP_404_NOT_FOUND
         return Message(message='Item not found')
      
      if item.qty < qty:
         response.status_code = status.HTTP_406_NOT_ACCEPTABLE
         return Message(message='No enough items in stock')
      
      cart_item = session.execute(select(CartItem).where(CartItem.cart_id == curr_user.cart.id, CartItem.item_id == item_id)).scalar()
      if cart_item == None:
         new_cart_item = CartItem(cost = qty * item.price, qty = qty, item = item, cart = curr_user.cart)
         session.add(new_cart_item)

      else:
         cart_item.qty += qty
         cart_item.cost = cart_item.qty * item.price
      
      curr_user.cart.cost += qty * item.price
      
      session.commit()
      return Message(message='Added to cart')
      
   except Exception as exc:
      session.rollback()
      logger.error(str(exc))
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(exc))
   
@router.get('/remove_from_cart/{item_id}/{qty}', response_model=Message)
async def remove_from_cart(item_id: int, qty: int, response: Response, user_id: int = Depends(authenticate_token), session: Session = Depends(get_session)):
   curr_user = validate_user(user_id=user_id, session=session)
   try:

      cart_item = session.execute(select(CartItem).where(CartItem.cart_id == curr_user.cart.id, CartItem.item_id == item_id)).scalar()
      if cart_item == None:
         response.status_code = status.HTTP_404_NOT_FOUND
         return Message(message='Product not found')
      
      qty = min(qty, cart_item.qty)

      cart_item.qty -= qty
      cart_item.cost -= qty * cart_item.item.price
      curr_user.cart.cost -= qty * cart_item.item.price

      if cart_item.qty <= 0:
         session.delete(cart_item)

      session.commit()
      return Message(message='Removed from cart')
      
   except Exception as exc:
      session.rollback()
      logger.error(str(exc))
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(exc))
   

@router.get('/show_cart', response_model=CartRead)
async def show_cart(user_id: int = Depends(authenticate_token), session: Session = Depends(get_session)):
   curr_user = validate_user(user_id=user_id, session=session)
   try:

      return curr_user.cart

   except Exception as exc:
      session.rollback()
      logger.error(str(exc))
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(exc))
   

@router.post('/submit_order', response_model= Message)
async def submit_order(response: Response, user_id: int = Depends(authenticate_token), session: Session = Depends(get_session)):
   curr_user = validate_user(user_id=user_id, session=session)
   try:

      if len(curr_user.cart.cart_items) == 0:
         response.status_code = status.HTTP_404_NOT_FOUND
         return Message(message='Empty cart')

      order = Order(user = curr_user)
      items = curr_user.cart.cart_items
      curr_user.cart.cost = 0

      for item in items:
         item.item.qty -= item.qty
         item.item.sale += item.qty
         
         order_item = OrderItem(cost = item.cost, qty = item.qty, item = item.item, order = order)
         order.cost += order_item.cost
         session.add(order_item)
         session.delete(item)
      
      session.add(order)
      session.commit()
      return Message(message='Order is submitted')

   except Exception as exc:
      session.rollback()
      logger.error(str(exc))
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.get('/show_orders', response_model= list[OrderRead])
async def show_orders(response: Response, user_id: int = Depends(authenticate_token), session: Session = Depends(get_session)):
   curr_user = validate_user(user_id=user_id, session=session)
   try:
      return curr_user.orders

   except Exception as exc:
      session.rollback()
      logger.error(str(exc))
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
   

@router.get('/get_popular_items/{limit}', response_model=list[ItemRead])
async def get_popular_products(limit: int, session: Session = Depends(get_session)):
   try:
      items = session.execute(
         select(Item).
         where(Item.deleted == False).limit(limit).order_by(desc(Item.sale))).scalars().fetchall()
      return items
   
   except Exception as exc:
      session.rollback()
      logger.error(str(exc))
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(exc))