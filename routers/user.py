from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.session import get_session
from utils.enums import Role
from utils.logger import logger
from utils.security import bcrypt_context, authenticate_token, validate_user
from schemas.user import UserCreate, UserRead, UserUpdate
from schemas.message import Message
from models.user import User
from models.payment import Payment
from models.cart import Cart

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/create_user", response_model=Message)
async def create_user(
    data: UserCreate, response: Response, session: Session = Depends(get_session)
):
    try:
        if (
            session.execute(select(User).where(User.username == data.username)).scalar()
            != None
        ):
            response.status_code = status.HTTP_409_CONFLICT
            return Message(message="Username already exist")
        if (
            session.execute(select(User).where(User.email == data.email)).scalar()
            != None
        ):
            response.status_code = status.HTTP_409_CONFLICT
            return Message(message="Email already exist")
        user = User(
            **data.model_dump(exclude=["password", "payment"]),
            password=bcrypt_context.hash(data.password),
            role=Role.USER,
        )
        payment = Payment(**data.payment.model_dump(), user=user)
        cart = Cart(user=user)

        session.add(user)
        session.add(payment)
        session.add(cart)

        session.commit()
        logger.info(f"User(id: {user.id}) is created")
        return Message(message="User is created")

    except Exception as exc:
        session.rollback()
        logger.error(str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.get("/get_user/{user_id}", response_model=UserRead | Message)
async def get_user(
    user_id: int, response: Response, session: Session = Depends(get_session)
):
    try:
        user = session.execute(select(User).where(User.id == user_id)).scalar()
        if user == None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return Message(message="User not found")

        return user

    except Exception as exc:
        session.rollback()
        logger.error(str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.get("/get_all_users/", response_model=list[UserRead])
async def get_all_user(session: Session = Depends(get_session)):
    try:
        all_users = session.execute(select(User)).scalars().fetchall()
        return all_users

    except Exception as exc:
        session.rollback()
        logger.error(str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.patch("/update_user", response_model=Message)
async def update_user(
    data: UserUpdate,
    user_id: int = Depends(authenticate_token),
    session: Session = Depends(get_session),
):
    curr_user = validate_user(user_id=user_id, session=session)
    try:
        for key, val in data.model_dump(exclude_unset=True).items():
            if key == "password":
                setattr(curr_user, key, bcrypt_context.hash(val))

            if key == "payment":
                for p_key, p_val in data.payment.model_dump(exclude_unset=True).items():
                    setattr(curr_user.payment, p_key, p_val)
            else:
                setattr(curr_user, key, val)

        session.commit()
        logger.info(f"User(id: {curr_user.id}) information is updated")
        return Message(message="User information is updated")

    except Exception as exc:
        session.rollback()
        logger.error(str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@router.delete("/delete_user", response_model=Message)
async def delete_user(
    user_id: int = Depends(authenticate_token), session: Session = Depends(get_session)
):
    curr_user = validate_user(user_id=user_id, session=session)
    try:
        session.delete(curr_user)
        session.commit()
        logger.info(f"User(id: {curr_user.id}) is deleted")
        return Message(message="User is deleted")

    except Exception as exc:
        session.rollback()
        logger.error(str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )