from functools import lru_cache
from fastapi import HTTPException, status
from database.config import Base, engine
from schemas.message import Message
from utils.logger import logger


class DatabaseService:
    def create_database(self) -> Message:
        try:
            Base.metadata.create_all(bind=engine)
            logger.info('Database is created')
            return Message(message='Database is created')

        except Exception as exc:
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
        

    def delete_database(self) -> Message:
        try:
            Base.metadata.drop_all(bind=engine)
            logger.info('Database is deleted')
            return Message(message='Database is deleted')

        except Exception as exc:
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
        
@lru_cache
def get_database_servicea():
    return DatabaseService()