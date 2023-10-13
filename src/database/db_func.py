import asyncio

from ulid import ulid
from src.database.models import UserSite, Product
from sqlalchemy import select


async def get_user(phone: str = None, user_id: str = None) -> UserSite:
    async with UserSite.async_session() as session:
        if phone:
            return await session.scalar(select(UserSite).filter(UserSite.phone == phone))
        if user_id:
            return await session.scalar(select(UserSite).filter(UserSite.id == user_id))


async def post_user(validate_user):
    async with UserSite.async_session() as session:
        user = UserSite(id=ulid(), **validate_user.model_dump())
        session.add(user)


async def select_emails() -> list[str]:
    async with UserSite.async_session() as session:
        result = await session.execute(select(UserSite.email))
        return [*result.scalars()]
        # return session.scalars(select(UserSite.email))


async def select_new_products() -> list:
    async with Product.async_session() as session:
        result = await session.execute(select(Product).filter(Product.is_new == True))
        return [*result.scalars()]
        # return session.scalars(select(Product).filter(Product.is_new == True))

