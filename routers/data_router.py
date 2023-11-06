from fastapi import APIRouter, Depends
from schemas.message import Message
from services.data_service import DataService, get_data_service

router = APIRouter(prefix='/api/data', tags=['Data'])

@router.post('', response_model=Message)
async def init_data(service: DataService = Depends(get_data_service)):
    return service.init_data()

@router.delete('', response_model=Message)
async def clear_data(service: DataService = Depends(get_data_service)):
    return service.clear_data()