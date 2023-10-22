from typing import Union

from fastapi import Depends, HTTPException, status, Cookie, Request, Path
from fastapi.responses import RedirectResponse
from sqlalchemy import select

from src.database.base import Base
from src.database.models import Product
from src.utils.jwt_auth import token_check
from src.validation.user_validators import UserView


async def _get_session():
    async with Base.async_session() as session:
        yield session


async def _is_user_authorized(request: Request) -> Union[None, UserView]:  # для страниц, которые доступны всем
    if not 'access_token' in request.cookies:
        return status.HTTP_401_UNAUTHORIZED
    return await token_check(token=request.cookies['access_token'])


async def _user_auth(access_token: str = Cookie(...)) -> Union[UserView, status.HTTP_401_UNAUTHORIZED]:  # для views
    user_or_401 = await token_check(token=access_token)
    if user_or_401 == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user_or_401


async def _get_product_info(slug: str = Path(default=..., min_length=3, max_length=64,
                                             examples=["big-stick", "lamp"])) -> Product:
    with Product.async_session() as session:
        product = await session.execute(select(Product).filter(Product.slug == slug))
        product = [*product.scalar()]
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product was not found")
    return product[0]


get_product_info = Depends(_get_product_info)
is_user_authorized = Depends(_is_user_authorized)
user_auth = Depends(_user_auth)
get_session = Depends(_get_session)
