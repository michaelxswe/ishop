from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_session
from schemas.message import Message
from schemas.order import OrderRead
from services.orders_service import OrdersService, get_orders_service
from utils.validation import authenticate_token

router = APIRouter(prefix='/api/orders', tags=['Orders'])
    

@router.post('', response_model=Message)
async def submit_order(user_id: int = Depends(authenticate_token), service: OrdersService = Depends(get_orders_service), session: Session = Depends(get_session)):
    return service.submit_order(user_id=user_id, session=session)
    

@router.get('', response_model=list[OrderRead])
async def show_orders(user_id: int = Depends(authenticate_token), service: OrdersService = Depends(get_orders_service), session: Session = Depends(get_session)):
    return service.show_orders(user_id=user_id, session=session)