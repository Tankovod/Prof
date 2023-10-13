from typing import Union, Optional

from fastapi import Depends, HTTPException, status, Cookie, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt
from src.database.base import Base
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from src.database.db_func import get_user
from src.database.models import UserSite
from src.utils.jwt_auth import token_check
from src.validation.user_validators import User, UserView
from src.validation.token_validators import TokenData
from src.validation.settings import settings

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# async def _get_db_session() -> AsyncSession:
#     with Base.async_session() as session:
#         yield session
#
#
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserSite:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     print(2222222222222222, token)
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY.unicode_string(),
#                              algorithms=[settings.ALGORITHM.unicode_string()])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#         token_data = TokenData(user_id=user_id)
#     except JWTError:
#         raise credentials_exception
#     user = await get_user(user_id=token_data.user_id)
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# async def _get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


async def _is_user_authorized(request: Request) -> Union[None, UserView]:  # для страниц, которые доступны всем пользователям
    if not 'access_token' in request.cookies:
        return
    print(request.cookies['access_token'])
    user_or_none = await token_check(token=request.cookies['access_token'])
    if not user_or_none:
        return
    return user_or_none


async def _user_auth_api(access_token: str = Cookie(...)) -> Union[status.HTTP_401_UNAUTHORIZED, UserView]:  # для api
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_or_401 = await token_check(token=access_token)
    if user_or_401 == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user_or_401


async def _user_auth_views(access_token: str = Cookie(...)) -> Union[status.HTTP_401_UNAUTHORIZED, UserView]:  # для views
    if not access_token:
        return RedirectResponse('/auth/login', status_code=status.HTTP_401_UNAUTHORIZED)
    user_or_401 = await token_check(token=access_token)
    if user_or_401 == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse('/auth/login', status_code=status.HTTP_401_UNAUTHORIZED)
    return user_or_401


is_user_authorized = Depends(_is_user_authorized)
user_auth_views = Depends(_user_auth_views)
user_auth_api = Depends(_user_auth_api)

