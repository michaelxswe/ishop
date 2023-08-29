from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_session
from schemas.token import Token
from schemas.user import UserCredentials
from services.security_service import SecurityService, get_security_service

router = APIRouter(prefix='/api/security', tags=['security'])


@router.post('/sign-in', response_model=Token)
async def sign_in(data: UserCredentials, service: SecurityService = Depends(get_security_service), session: Session = Depends(get_session)):
    return service.sign_in(data = data, session = session)