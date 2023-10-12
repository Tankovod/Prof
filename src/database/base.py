from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import Column, INT
from src.validation.settings import settings


class Base(DeclarativeBase):
    async_engine = create_async_engine(url=settings.DATABASE_ASYNC_URL.unicode_string())
    async_session = async_sessionmaker(bind=async_engine)

    id = Column(INT, primary_key=True)



