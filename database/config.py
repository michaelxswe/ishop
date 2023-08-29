from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from utils.settings import POSTGRES_USER, POSTGRES_PASSWORD, ENDPOINT, PORT, DB

DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{ENDPOINT}:{PORT}/{DB}'
engine = create_engine(url = DB_URL, echo=True)

class Base(DeclarativeBase, MappedAsDataclass):
    pass