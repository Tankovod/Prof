import asyncio

from ulid import ulid
from src.database.models import UserSite
from sqlalchemy import select


async def get_user(phone: str = None, user_id: str = None) -> UserSite:
    async with UserSite.async_session() as session:
        if phone:
            return await session.scalar(select(UserSite).filter(UserSite.phone == phone))
        if user_id:
            return await session.scalar(select(UserSite).filter(UserSite.id == user_id))


async def post_user(validate_user):
    async with UserSite.async_session() as session:
        async with session.begin():
            user = UserSite(id=ulid(), **validate_user.model_dump())
            session.add(user)


# asyncio.run(get_user('sdfgdsf'))