from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_session
from utils.logger import logger
from utils.security import authenticate_user, create_token
from schemas.token import Token
from schemas.user import UserCredentials

router = APIRouter(prefix="/api/security", tags=["security"])


@router.post("/sign_in", response_model=Token)
async def sign_in(data: UserCredentials, session: Session = Depends(get_session)):
    user_id = authenticate_user(
        username=data.username, password=data.password, session=session
    )

    if user_id == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_token(user_id=user_id)
    logger.info(f"User(id: {user_id}) signed in")
    return Token(access_token=token, token_type="bearer")