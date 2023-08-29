from functools import lru_cache
from fastapi import HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from models.cart import Cart
from models.cart_item import CartItem
from models.item import Item
from models.order import Order
from models.order_item import OrderItem
from schemas.item import ItemCreate
from schemas.message import Message
from utils.logger import logger
from utils.security import get_curr_user


class ItemService:
    def add_item(self, data: ItemCreate, session: Session) -> Message:
        try:
            if session.execute(select(Item).where(Item.name == data.name)).scalar() != None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Item already exist')

            item = Item(**data.model_dump())
            session.add(item)
            session.commit()
            logger.info(f'Item(id: {item.id}) is added')
            return Message(message='Item is added')

        except HTTPException as exc:
            raise

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
      
    def get_item(self, item_id: int, session: Session) -> Item:
        try:
            item = session.execute(select(Item).where(Item.id == item_id, Item.deleted == False)).scalar()

            if item == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

            return item

        except HTTPException as exc:
            raise

        except Exception as exc:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
        
    def get_all_items(self, session: Session) -> list[Item]:
        try:
            all_products = (session.execute(select(Item).where(Item.deleted == False)).scalars().fetchall())
            return all_products

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    
    def add_to_cart(self, item_id: int, qty: int, user_id: int, session: Session) -> Message:
        try:
            curr_user = get_curr_user(user_id=user_id, session=session)

            item = session.execute(select(Item).where(Item.id == item_id, Item.deleted == False)).scalar()

            if item == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'Item not found')

            if item.qty < qty:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Not enough items in stock')

            cart_item = session.execute(select(CartItem).where(CartItem.cart_id == curr_user.cart.id, CartItem.item_id == item_id)).scalar()
            if cart_item == None:
                new_cart_item = CartItem(cost=qty * item.price, qty=qty, item=item, cart=curr_user.cart)
                session.add(new_cart_item)

            else:
                cart_item.qty += qty
                cart_item.cost = cart_item.qty * item.price

            curr_user.cart.cost += qty * item.price

            session.commit()
            return Message(message='Added to cart')
        
        except HTTPException as exc:
            raise

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
      
    def remove_from_cart(self, item_id: int, qty: int, user_id: int, session: Session) -> Message:
        try:
            curr_user = get_curr_user(user_id=user_id, session=session)
            cart_item = session.execute(select(CartItem).where(CartItem.cart_id == curr_user.cart.id, CartItem.item_id == item_id)).scalar()
            
            if cart_item == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

            qty = min(qty, cart_item.qty)

            cart_item.qty -= qty
            cart_item.cost -= qty * cart_item.item.price
            curr_user.cart.cost -= qty * cart_item.item.price

            if cart_item.qty <= 0:
                session.delete(cart_item)

            session.commit()
            return Message(message='Removed from cart')
        
        except HTTPException as exc:
            raise

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    
    def clear_cart(self, user_id: int, session: Session) -> Message:
        try:
            curr_user = get_curr_user(user_id=user_id, session=session)
            
            for cart_item in curr_user.cart.cart_items:
                session.delete(cart_item)

            curr_user.cart.cost = 0
            session.commit()
            return Message(message='Car items are cleared')

        except HTTPException as exc:
            raise

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    
    def show_cart(self, user_id: int, session: Session) -> Cart:
        try:
            curr_user = get_curr_user(user_id=user_id, session=session)
            return curr_user.cart

        except HTTPException as exc:
            raise

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    def submit_order(self, user_id: int, session: Session) -> Message:
        try:
            curr_user = get_curr_user(user_id=user_id, session=session)
            if len(curr_user.cart.cart_items) == 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Empty Cart')

            order = Order(user=curr_user)
            items = curr_user.cart.cart_items
            curr_user.cart.cost = 0

            for item in items:
                item.item.qty -= item.qty
                item.item.sale += item.qty

                order_item = OrderItem(
                    cost=item.cost, qty=item.qty, item=item.item, order=order
                )
                order.cost += order_item.cost
                session.add(order_item)
                session.delete(item)

            session.add(order)
            session.commit()
            return Message(message='Order is submitted')

        except HTTPException as exc:
            raise

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
        
    def show_orders(self, user_id: int, session: Session) -> list[Order]:
        try:
            curr_user = get_curr_user(user_id=user_id, session=session)
            return curr_user.orders

        except HTTPException as exc:
            raise

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    
    def get_popular_items(self, limit: int, session: Session) -> list[Item]:
        try:
            items = (session.execute(select(Item).where(Item.deleted == False).limit(limit).order_by(desc(Item.sale))).scalars().fetchall())
            return items

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
        
    
@lru_cache
def get_item_service():
    return ItemService()