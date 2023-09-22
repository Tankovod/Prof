from fastapi import Depends, HTTPException, status
from typing_extensions import Annotated
from jose import JWTError, jwt
from src.database.base import Base
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from src.database.db_func import get_user
from src.types_.types__ import User, TokenData
from src.types_.settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def _get_db_session() -> Session:
    with Base.async_session() as session:
        yield session


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = await get_user(user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def _get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


get_db_session = Depends(_get_db_session)
get_current_active_user = Depends(_get_current_active_user)
