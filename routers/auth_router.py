from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_session
from schemas.token import Token
from schemas.user import UserCredentials
from services.auth_service import AuthService, get_auth_service

router = APIRouter(prefix='/api/auth', tags=['Auth'])


@router.post('/sign-in', response_model=Token)
async def sign_in(data: UserCredentials, service: AuthService = Depends(get_auth_service), session: Session = Depends(get_session)):
    return service.sign_in(data = data, session = session)