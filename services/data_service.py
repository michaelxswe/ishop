from functools import lru_cache
from fastapi import HTTPException, status
from database.config import Base, engine
from schemas.message import Message
from utils.logger import logger


class DataService:
    def init_data(self) -> Message:
        try:
            Base.metadata.create_all(bind=engine)
            message = 'Data is initalized'
            logger.info(message)
            return Message(message=message)

        except Exception as exc:
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
        

    def clear_data(self) -> Message:
        try:
            Base.metadata.drop_all(bind=engine)
            message = 'Data is cleared'
            logger.info(message)
            return Message(message=message)

        except Exception as exc:
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
        
@lru_cache
def get_data_service():
    return DataService()