from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_session
from schemas.item import ItemCreate, ItemRead
from schemas.message import Message
from services.items_service import ItemsService, get_items_service

router = APIRouter(prefix='/api/items', tags=['Items'])

@router.post('', response_model=Message)
async def add_item(data: ItemCreate, service: ItemsService = Depends(get_items_service), session: Session = Depends(get_session)):
    return service.add_item(data=data, session=session)
    

@router.get('/{item_id}', response_model=ItemRead)
async def get_item(item_id: int, service: ItemsService = Depends(get_items_service), session: Session = Depends(get_session)):
    return service.get_item(item_id=item_id, session=session)
    

@router.get('', response_model=list[ItemRead])
async def get_items(service: ItemsService = Depends(get_items_service), session: Session = Depends(get_session)):
    return service.get_items(session=session)


@router.get('/popular/{limit}', response_model=list[ItemRead])
async def get_popular_items(limit: int, service: ItemsService = Depends(get_items_service), session: Session = Depends(get_session)):
    return service.get_popular_items(limit=limit, session=session)