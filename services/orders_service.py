from functools import lru_cache
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.order import Order
from models.order_item import OrderItem
from schemas.message import Message
from utils.logger import logger
from utils.validation import get_curr_user


class OrdersService:
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
    
@lru_cache
def get_orders_service():
    return OrdersService()