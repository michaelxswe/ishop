from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_session
from schemas.message import Message
from schemas.user import UserCreate, UserRead, UserUpdate
from services.user_serivce import UserService, get_user_service
from utils.security import authenticate_token

router = APIRouter(prefix='/api/user', tags=['user'])

@router.post('/create-user', response_model=Message)
async def create_user(data: UserCreate, service: UserService = Depends(get_user_service), session: Session = Depends(get_session)):
    return service.create_user(data = data, session=session)


@router.get('/get-user/{user_id}', response_model=UserRead)
async def get_user(user_id: int, service: UserService = Depends(get_user_service), session: Session = Depends(get_session)):
    return service.get_user(user_id=user_id, session=session)
    

@router.get('/get-all-users/', response_model=list[UserRead])
async def get_all_users(service: UserService = Depends(get_user_service), session: Session = Depends(get_session)):
    return service.get_all_users(session=session)


@router.patch('/update-user', response_model=Message)
async def update_user(data: UserUpdate, user_id: int = Depends(authenticate_token), service: UserService = Depends(get_user_service), session: Session = Depends(get_session)):
    return service.update_user(data = data, user_id=user_id, session=session)


@router.delete('/delete-user', response_model=Message)
async def delete_user(user_id: int = Depends(authenticate_token), service: UserService = Depends(get_user_service), session: Session = Depends(get_session)):
    return service.delete_user(user_id=user_id, session=session)