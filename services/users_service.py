from functools import lru_cache
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.cart import Cart
from models.payment import Payment
from models.user import User
from schemas.message import Message
from schemas.user import UserCreate, UserUpdate
from common.enums import Role
from utils.logger import logger
from utils.validation import bcrypt_context, get_curr_user


class UsersService:

    def create_user(self, data: UserCreate, session: Session) -> Message:
        try:
            if (session.execute(select(User).where(User.username == data.username)).scalar()!= None):           
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exist')
                
            if (session.execute(select(User).where(User.email == data.email)).scalar()!= None):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Email already exist')

            user = User(**data.model_dump(exclude=['password', 'payment']), password=bcrypt_context.hash(data.password), role=Role.USER)
            payment = Payment(**data.payment.model_dump(), user=user)
            cart = Cart(user=user)

            session.add(user)
            session.add(payment)
            session.add(cart)

            session.commit()
            logger.info(f'User(id: {user.id}) is created')
            return Message(message='User is created')
        
        except HTTPException as exc:
            raise

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')
        
    def get_user(self, user_id: int, session: Session) -> User:
        try:
            user = session.execute(select(User).where(User.id == user_id)).scalar()
            if user == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

            return user

        except HTTPException as exc:
            raise

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    
    def get_users(self, session: Session) -> list[User]:
        try:
            users = session.execute(select(User)).scalars().fetchall()
            return users

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
        
    def update_user(self, data: UserUpdate, user_id: int, session: Session) -> Message:
        try:
            curr_user = get_curr_user(user_id=user_id, session=session)
            for key, val in data.model_dump(exclude_unset=True).items():
                if key == 'password':
                    setattr(curr_user, key, bcrypt_context.hash(val))

                if key == 'payment':
                    for p_key, p_val in data.payment.model_dump(exclude_unset=True).items():
                        setattr(curr_user.payment, p_key, p_val)
                else:
                    setattr(curr_user, key, val)

            session.commit()
            logger.info(f'User(id: {curr_user.id}) information is updated')
            return Message(message='User information is updated')

        except HTTPException as exc:
            raise

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    
    def delete_user(self, user_id: int, session: Session) -> Message:
        try:
            curr_user = get_curr_user(user_id=user_id, session=session)
            session.delete(curr_user)
            session.commit()
            logger.info(f'User(id: {curr_user.id}) is deleted')
            return Message(message='User is deleted')
        
        except HTTPException as exc:
            raise

        except Exception as exc:
            session.rollback()
            logger.error(str(exc))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
        
@lru_cache
def get_users_service():
    return UsersService()