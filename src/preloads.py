import asyncio
from src.database.models import UserSite
from ulid import ulid
from src.utils.jwt_auth import get_password_hash
from src.types_.types__ import User


async def async_main():
    async with UserSite.async_session() as session:
        async with session.begin():
            user = UserSite(id=ulid(), **User(password=await get_password_hash('Tralolo1243y'), email='sdfgdd@mail.com',
                                   phone='+348362497234798', disabled=False, first_name=None, last_name=None).model_dump())
            session.add(user)


asyncio.run(async_main())