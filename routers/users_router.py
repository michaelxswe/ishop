from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_session
from schemas.message import Message
from schemas.user import UserCreate, UserRead, UserUpdate
from services.users_service import UsersService, get_users_service
from utils.validation import authenticate_token

router = APIRouter(prefix='/api/users', tags=['Users'])

@router.post('', response_model=Message)
async def create_user(data: UserCreate, service: UsersService = Depends(get_users_service), session: Session = Depends(get_session)):
    return service.create_user(data = data, session=session)


@router.get('/{user_id}', response_model=UserRead)
async def get_user(user_id: int, service: UsersService = Depends(get_users_service), session: Session = Depends(get_session)):
    return service.get_user(user_id=user_id, session=session)
    

@router.get('', response_model=list[UserRead])
async def get_users(service: UsersService = Depends(get_users_service), session: Session = Depends(get_session)):
    return service.get_users(session=session)


@router.patch('', response_model=Message)
async def update_user(data: UserUpdate, user_id: int = Depends(authenticate_token), service: UsersService = Depends(get_users_service), session: Session = Depends(get_session)):
    return service.update_user(data = data, user_id=user_id, session=session)


@router.delete('', response_model=Message)
async def delete_user(user_id: int = Depends(authenticate_token), service: UsersService = Depends(get_users_service), session: Session = Depends(get_session)):
    return service.delete_user(user_id=user_id, session=session)