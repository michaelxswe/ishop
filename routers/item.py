from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_session
from schemas.cart import CartRead
from schemas.item import ItemCreate, ItemRead
from schemas.message import Message
from schemas.order import OrderRead
from services.item_service import ItemService, get_item_service
from utils.security import authenticate_token

router = APIRouter(prefix='/api/item', tags=['item'])


@router.post('/add-item', response_model=Message)
async def add_item(data: ItemCreate, service: ItemService = Depends(get_item_service), session: Session = Depends(get_session)):
    return service.add_item(data=data, session=session)
    

@router.get('/get-item/{item_id}', response_model=ItemRead)
async def get_item(item_id: int, service: ItemService = Depends(get_item_service), session: Session = Depends(get_session)):
    return service.get_item(item_id=item_id, session=session)
    

@router.get('/get-all-items', response_model=list[ItemRead])
async def get_all_items(service: ItemService = Depends(get_item_service), session: Session = Depends(get_session)):
    return service.get_all_items(session=session)


@router.get('/add-to-cart/{item_id}/{qty}', response_model=Message)
async def add_to_cart(item_id: int, qty: int, user_id: int = Depends(authenticate_token), service: ItemService = Depends(get_item_service), session: Session = Depends(get_session)):
    return service.add_to_cart(item_id=item_id, qty=qty, user_id=user_id, session=session)
    

@router.get('/remove-from-cart/{item_id}/{qty}', response_model=Message)
async def remove_from_cart(item_id: int, qty: int, user_id: int = Depends(authenticate_token), service: ItemService = Depends(get_item_service), session: Session = Depends(get_session)):
    return service.remove_from_cart(item_id=item_id, qty=qty, user_id=user_id, session=session)


@router.get('/clear-cart/', response_model=Message)
async def clear_cart(user_id: int = Depends(authenticate_token), service: ItemService = Depends(get_item_service), session: Session = Depends(get_session)):
    return service.clear_cart(user_id=user_id, session=session)
    

@router.get('/show-cart', response_model=CartRead)
async def show_cart(user_id: int = Depends(authenticate_token), service: ItemService = Depends(get_item_service), session: Session = Depends(get_session)):
    return service.show_cart(user_id=user_id, session=session)
    

@router.post('/submit-order', response_model=Message)
async def submit_order(user_id: int = Depends(authenticate_token), service: ItemService = Depends(get_item_service), session: Session = Depends(get_session)):
    return service.submit_order(user_id=user_id, session=session)
    

@router.get('/show-orders', response_model=list[OrderRead])
async def show_orders(user_id: int = Depends(authenticate_token), service: ItemService = Depends(get_item_service), session: Session = Depends(get_session)):
    return service.show_orders(user_id=user_id, session=session)


@router.get('/get-popular-items/{limit}', response_model=list[ItemRead])
async def get_popular_items(limit: int, service: ItemService = Depends(get_item_service), session: Session = Depends(get_session)):
    return service.get_popular_items(limit=limit, session=session)