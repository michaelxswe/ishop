from sqlalchemy.orm import sessionmaker, Session
from db.config import engine

SessionClass = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Session:
    try:
      session = SessionClass()
      yield session
    finally:
       session.close()