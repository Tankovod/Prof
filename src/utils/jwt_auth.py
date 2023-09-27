from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from typing import Annotated

from sqlalchemy import select

from src.database.db_func import get_user
from src.database.models import UserSite
from src.dependencies import get_db_session
from src.settings import pwd_context
from src.types_.settings import Settings
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.types_.types__ import User, TokenData


async def get_password_hash(password):
    return pwd_context.hash(password)


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(phone: str, password: str):
    user = await get_user(phone=phone)
    if not user:
        return False
    if not await verify_password(password, user.password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    access_token = {'access_token': encoded_jwt, 'expire_in': datetime.timestamp(expire)}
    return access_token


async def token_check(token):
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
    except Exception as ex:
        return status.HTTP_401_UNAUTHORIZED
    user_id = payload.get('sub')
    user_id = await get_user(user_id=user_id)
    if not user_id:
        return status.HTTP_401_UNAUTHORIZED


async def get_user_id(token):
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
    except Exception as ex:
        return status.HTTP_401_UNAUTHORIZED
    return payload.get('sub')
