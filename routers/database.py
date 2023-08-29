from fastapi import APIRouter, Depends
from schemas.message import Message
from services.database_service import DatabaseService, get_database_servicea

router = APIRouter(prefix='/api/database', tags=['database'])

@router.get('/create-database', response_model=Message)
async def create_database(service: DatabaseService = Depends(get_database_servicea)):
    return service.create_database()

@router.get('/delete-database', response_model=Message)
async def delete_database(service: DatabaseService = Depends(get_database_servicea)):
    return service.delete_database()