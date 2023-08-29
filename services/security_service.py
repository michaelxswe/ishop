from functools import lru_cache
from sqlalchemy.orm import Session
from schemas.token import Token
from schemas.user import UserCredentials
from utils.logger import logger
from utils.security import authenticate_user, create_token


class SecurityService:
    def sign_in(self, data: UserCredentials, session: Session) -> Token:
        user_id = authenticate_user(username=data.username, password=data.password, session=session)
        token = create_token(user_id = user_id)
        logger.info(f'User(id: {user_id}) signed in')
        return Token(access_token=token, token_type='bearer')
      
@lru_cache
def get_security_service():
    return SecurityService()