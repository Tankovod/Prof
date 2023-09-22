from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import Column, INT
from src.types_.settings import Settings


class Base(DeclarativeBase):
    async_engine = create_async_engine(url=Settings.DATABASE_URL)
    async_session = async_sessionmaker(bind=async_engine)

    id = Column(INT, primary_key=True)



