from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models.user import User
from utils.settings import SECRET_KEY, ALGORITHM, TOKEN_EXPIRATION_TIME_IN_MIN

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
http_bearer = HTTPBearer()

def authenticate_user(username: str, password: str, session: Session) -> int:
    user = session.execute(select(User).where(User.username == username)).scalar()

    if user == None or bcrypt_context.verify(password, user.password) == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

    return user.id


def get_curr_user(user_id: int, session: Session) -> User:
    user = session.execute(select(User).where(User.id == user_id)).scalar()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


def create_token(user_id: int) -> str:
    encode = {"user_id": user_id}
    expires = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_IN_MIN)
    encode.update({"exp": expires})
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def authenticate_token(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> int:
    try:
        token = credentials.credentials
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_token.get("user_id")

        return user_id

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
