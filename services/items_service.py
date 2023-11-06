from functools import lru_cache
from fastapi import HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from models.item import Item
from schemas.item import ItemCreate
from schemas.message import Message
from utils.logger import logger


class ItemsService:
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
        
    def get_items(self, session: Session) -> list[Item]:
        try:
            items = (session.execute(select(Item).where(Item.deleted == False)).scalars().fetchall())
            return items

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
def get_items_service():
    return ItemsService()