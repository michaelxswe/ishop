from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_session
from schemas.cart import CartRead
from schemas.message import Message
from services.cart_service import CartService, get_cart_service
from utils.validation import authenticate_token

router = APIRouter(prefix='/api/cart', tags=['Cart'])


@router.post('/{item_id}/{qty}', response_model=Message)
async def add_to_cart(item_id: int, qty: int, user_id: int = Depends(authenticate_token), service: CartService = Depends(get_cart_service), session: Session = Depends(get_session)):
    return service.add_to_cart(item_id=item_id, qty=qty, user_id=user_id, session=session)
    

@router.delete('/{item_id}/{qty}', response_model=Message)
async def remove_from_cart(item_id: int, qty: int, user_id: int = Depends(authenticate_token), service: CartService = Depends(get_cart_service), session: Session = Depends(get_session)):
    return service.remove_from_cart(item_id=item_id, qty=qty, user_id=user_id, session=session)


@router.delete('', response_model=Message)
async def clear_cart(user_id: int = Depends(authenticate_token), service: CartService = Depends(get_cart_service), session: Session = Depends(get_session)):
    return service.clear_cart(user_id=user_id, session=session)
    

@router.get('', response_model=CartRead)
async def show_cart(user_id: int = Depends(authenticate_token), service: CartService = Depends(get_cart_service), session: Session = Depends(get_session)):
    return service.show_cart(user_id=user_id, session=session)